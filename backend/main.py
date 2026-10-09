from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, Date
from database import engine, Base, get_db
import models
from schemas import ProductCreate, CheckoutRequest, InventoryResponse
from datetime import datetime
LOW_STOCK_THRESHOLD = 5

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Retail Intelligence Platform API"}


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products
    

@app.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=product.name,
        barcode=product.barcode,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
    

@app.get("/products/{id}")
def get_product_id(id: int, db:Session=Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id==id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product Not found")
    else:
        return product


@app.post("/checkout")
def checkout(request:CheckoutRequest, db:Session=Depends(get_db)):
    if not request.items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
    )
    total=0
    try:
        for item in request.items:
            product=db.query(models.Product).filter(models.Product.id == item.product_id).first()
            if product is None:
                raise HTTPException(status_code=404, detail="404 not found")

            if product.stock<item.quantity:
                raise HTTPException(status_code=400, detail="Not enough stock")
            total+=item.quantity*product.price

        transaction=models.Transaction(
            total=total,
            sold_at=datetime.now()
            )
        db.add(transaction)
        db.flush()

        for item in request.items:
            product=db.query(models.Product).filter(models.Product.id == item.product_id).first()
            transaction_item=models.TransactionItem(
                transaction_id=transaction.transaction_id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )
            db.add(transaction_item)
            product.stock-=item.quantity
        db.commit()
        return{
            "message": "Transaction Successful",
            "transaction_id": transaction.transaction_id,
            "total": total

        }

    except Exception:
        db.rollback()
        raise

@app.get("/inventory",response_model=list[InventoryResponse])
def get_inventory(db:Session=Depends(get_db)):
    result=[]
    inventory=db.query(
        models.Product.id,
        models.Product.name,
        models.Product.stock
        ).all()
    for item in inventory:
        if item.stock<=LOW_STOCK_THRESHOLD:
            status="LOW"
        else:
            status="OK"

        inventory_item=InventoryResponse(
            id=item.id,
            name=item.name,
            stock=item.stock,
            status=status
        )
        result.append(inventory_item)
    return result

@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    result=[]
    
    for transaction_record in transactions:
        transaction_items = db.query(models.TransactionItem).filter(
        models.TransactionItem.transaction_id == transaction_record.transaction_id
        ).all()
        items_data = []

        for item_record in transaction_items:
            product_record = db.query(models.Product).filter(
            models.Product.id == item_record.product_id
            ).first()
            item_data = {
            "product_name": product_record.name,
            "quantity": item_record.quantity,
            "price": item_record.price
            }
            items_data.append(item_data)
        
        transaction_data = {
        "transaction_id": transaction_record.transaction_id,
        "total": transaction_record.total,
        "sold_at": transaction_record.sold_at,
        "items": items_data
}

        result.append(transaction_data)
    return result

@app.get("/analytics/sales")
def get_sales_analytics(db: Session = Depends(get_db)):
    total_revenue = db.query(
        func.sum(models.Transaction.total)
    ).scalar()

    total_transactions = db.query(
        func.count(models.Transaction.transaction_id)
    ).scalar()

    total_units_sold = db.query(
    func.sum(models.TransactionItem.quantity)
    ).scalar()

    top_products = db.query(
    models.Product.id,
    models.Product.name,
    func.sum(models.TransactionItem.quantity).label("units_sold")
    ).join(
    models.TransactionItem,
    models.Product.id == models.TransactionItem.product_id
    ).group_by(
    models.Product.id,
    models.Product.name
    ).order_by(
    func.sum(models.TransactionItem.quantity).desc()).limit(5).all()

    top_products_data = []

    for product_id, product_name, units_sold in top_products:
        top_products_data.append({
            "product_id": product_id,
            "product_name": product_name,
            "units_sold": units_sold
    })

    hourly_sales = db.query(
    extract("hour", models.Transaction.sold_at),
    func.sum(models.Transaction.total).label("revenue")
    ).group_by(
    extract("hour", models.Transaction.sold_at)
    ).order_by(
    extract("hour", models.Transaction.sold_at)
        ).all()

    hourly_sales_data = []

    for hour, revenue in hourly_sales:
        hourly_sales_data.append({
        "hour": hour,
        "revenue": revenue
    })

    daily_sales = db.query(
    models.Transaction.sold_at.cast(Date),
    func.sum(models.Transaction.total).label("revenue")
    ).group_by(
    models.Transaction.sold_at.cast(Date)
    ).order_by( models.Transaction.sold_at.cast(Date)).all()

    daily_sales_data = []

    for date, revenue in daily_sales:
        daily_sales_data.append({
        "date": date,
        "revenue": revenue
    })
    
    return {
        "total_revenue": total_revenue,
        "total_transactions": total_transactions,
        "total_units_sold": total_units_sold,
        "top_products": top_products_data,
        "hourly_sales": hourly_sales_data,
        "daily_sales": daily_sales_data
    }    
    
        
            

        

    
        
    

       
   
  
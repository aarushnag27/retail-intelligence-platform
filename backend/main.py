from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
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
            "Transaction Id": transaction.transaction_id,
            "Total": total

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
    
    
    
        
            

        

    
        
    

       
   
  
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from schemas import ProductCreate

app = FastAPI()

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
   
  
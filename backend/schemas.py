from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    barcode: str
    price: float
    stock: int
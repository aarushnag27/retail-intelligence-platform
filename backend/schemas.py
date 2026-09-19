from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    barcode: str
    price: float
    stock: int


class CartItem(BaseModel):
    product_id: int
    quantity:int

class CheckoutRequest(BaseModel):
    items: list[CartItem]
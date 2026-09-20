from pydantic import BaseModel, PositiveInt


class ProductCreate(BaseModel):
    name: str
    barcode: str
    price: float
    stock: int


class CartItem(BaseModel):
    product_id: int
    quantity:PositiveInt

class CheckoutRequest(BaseModel):
    items: list[CartItem]
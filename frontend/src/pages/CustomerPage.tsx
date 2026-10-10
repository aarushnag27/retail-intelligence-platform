import { useEffect, useState } from "react"
import "./RetailPages.css"
type Product = {
  id: number
  name: string
  price: number
  stock: number
}

type CartItem = {
  product_id: number
  quantity: number
}

function CustomerPage() {
 useEffect(() => {
  fetch("http://127.0.0.1:8000/products")
  .then(response => response.json())
  .then(data => setProducts(data))
}, [])
const [products, setProducts] = useState<Product[]>([])
const [cart, setCart] = useState<CartItem[]>([])
const [stockMessages, setStockMessages] = useState<Record<number, string>>({})
const [checkoutMessage, setCheckoutMessage] = useState("")

function addToCart(productId: number) {
  const product = products.find(product => product.id === productId)

  if (!product) {
    return
  }

  const cartItem = cart.find(item => item.product_id === productId)
  setStockMessages(currentMessages => ({
    ...currentMessages,
    [productId]: (cartItem ? cartItem.quantity >= product.stock : product.stock === 0)
      ? "Not enough stock — can't add the product."
      : ""
  }))

  setCart(currentCart => {
    const existingItem = currentCart.find(
      item => item.product_id === productId
    )

    if (existingItem) {
      if (existingItem.quantity >= product.stock) {
        return currentCart
      }

      return currentCart.map(item =>
        item.product_id === productId
          ? { ...item, quantity: item.quantity + 1 }
          : item
      )
    }

    if (product.stock === 0) {
      return currentCart
    }

    return [
      ...currentCart,
      {
        product_id: productId,
        quantity: 1
      }
    ]
  })
}

function updateQuantity(productId: number, change: number) {
  const product = products.find(product => product.id === productId)

  if (!product) {
    return
  }

  const cartItem = cart.find(item => item.product_id === productId)
  setStockMessages(currentMessages => ({
    ...currentMessages,
    [productId]: cartItem && cartItem.quantity + change > product.stock
      ? "Not enough stock — can't add the product."
      : ""
  }))

  setCart(currentCart => {
    return currentCart
      .map(item => {
        if (item.product_id !== productId) {
          return item
        }

        const newQuantity = item.quantity + change

        if (newQuantity > product.stock) {
          return item
        }

        return {
          ...item,
          quantity: newQuantity
        }
      })
      .filter(item => item.quantity > 0)
  })
}

function getProduct(productId: number) {
  return products.find(product => product.id === productId)
}

async function checkout() {
  setCheckoutMessage("")
  const response = await fetch("http://127.0.0.1:8000/checkout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      items: cart
    })
  })
  if (!response.ok) {
  const errorData = await response.json()
  setCheckoutMessage(errorData.detail)
  return
}

  const data = await response.json()

  setCheckoutMessage(
  `${data.message} — Transaction #${data.transaction_id} — ₹${data.total}`
  
)
setCheckoutMessage(
  `${data.message} — Transaction #${data.transaction_id} — ₹${data.total}`
)
setCart([])


  const productsResponse = await fetch(
    "http://127.0.0.1:8000/products"
  )

  const updatedProducts = await productsResponse.json()

  setProducts(updatedProducts)
}

const cartTotal = cart.reduce((total, item) => {
  const product = getProduct(item.product_id)

  if (!product) {
    return total
  }

  return total + product.price * item.quantity
}, 0)

  return (
  <main className="retail-page customer-page">
    <header className="retail-header">
      <p className="retail-eyebrow">Retail Intelligence Platform</p>
      <h1>Customer Checkout</h1>
      <p className="retail-description">Browse products, build your cart, and complete your purchase.</p>
    </header>

    <section className="retail-catalog" aria-labelledby="products-heading">
      <div className="retail-section-heading">
        <h2 id="products-heading">Products</h2>
        <p className="retail-description">Choose products to add to your cart.</p>
      </div>
      <div className="retail-product-grid">

    {products.map(product => (
      <div className="retail-card retail-product" key={product.id}>
        <h3>{product.name}</h3>
        <p className="retail-price">₹{product.price}</p>

        <button className="retail-button retail-button--secondary" onClick={() => addToCart(product.id)}>
          Add to Cart
        </button>
        {stockMessages[product.id] && (
          <p className="retail-message retail-message--error" role="status">{stockMessages[product.id]}</p>
        )}
      </div>
    ))}
      </div>
    </section>

    <section className="retail-card retail-checkout" aria-labelledby="cart-heading">
      <div className="retail-section-heading">
        <p className="retail-eyebrow">Current order</p>
        <h2 id="cart-heading">Cart</h2>
      </div>
      <div className="retail-cart-items">

   {cart.map(item => {
  const product = getProduct(item.product_id)

  if (!product) {
    return null
  }

  

  return (
    <div className="retail-cart-item" key={item.product_id}>
      <div className="retail-cart-details">
        <h3>{product.name}</h3>
        <p className="retail-description">₹{product.price} · Quantity: {item.quantity}</p>
      </div>

      <div className="retail-quantity-controls">
      <button className="retail-button retail-quantity-button" aria-label={`Decrease quantity of ${product.name}`} onClick={() => updateQuantity(item.product_id, -1)}>
        -
      </button>

      <button className="retail-button retail-quantity-button" aria-label={`Increase quantity of ${product.name}`} onClick={() => updateQuantity(item.product_id, 1)}>
        +
      </button>
      </div>
    </div>
  )
})}
      </div>
<p className="retail-cart-total"><span>Cart Total</span><strong>₹{cartTotal}</strong></p>

<button className="retail-button retail-button--primary" onClick={checkout}>
  Checkout
</button>
{checkoutMessage && <p className="retail-message">{checkoutMessage}</p>}


    </section>
  </main>
)
  }

export default CustomerPage

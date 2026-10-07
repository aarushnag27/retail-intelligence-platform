import { useEffect, useState } from "react"
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

function App() {
 useEffect(() => {
  fetch("http://127.0.0.1:8000/products")
  .then(response => response.json())
  .then(data => setProducts(data))
}, [])
const [products, setProducts] = useState<Product[]>([])
const [cart, setCart] = useState([])

function addToCart(productId: number) {
  const product = products.find(product => product.id === productId)

  if (!product) {
    return
  }

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
  const response = await fetch("http://127.0.0.1:8000/checkout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      items: cart
    })
  })

  const data = await response.json()

  console.log(data)

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
  <div>
    <h1>Retail Intelligence Platform</h1>

    {products.map(product => (
      <div key={product.id}>
        <p>
          {product.name} - ₹{product.price} - Stock: {product.stock}
        </p>

        <button onClick={() => addToCart(product.id)}>
          Add to Cart
        </button>
      </div>
    ))}

    <h2>Cart</h2>

   {cart.map(item => {
  const product = getProduct(item.product_id)

  if (!product) {
    return null
  }

  

  return (
    <div key={item.product_id}>
      <p>
        {product.name} - ₹{product.price} - Quantity: {item.quantity}
      </p>

      <button onClick={() => updateQuantity(item.product_id, -1)}>
        -
      </button>

      <button onClick={() => updateQuantity(item.product_id, 1)}>
        +
      </button>
    </div>
  )
})}
<p>Cart Total: ₹{cartTotal}</p>

<button onClick={checkout}>
  Checkout
</button>


  </div>
)
  }

export default App
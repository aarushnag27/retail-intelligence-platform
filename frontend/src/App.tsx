import { useEffect, useState } from "react"
type Product = {
  id: number
  name: string
  price: number
  stock: number
}
function App() {
 useEffect(() => {
  fetch("http://127.0.0.1:8000/products")
  .then(response => response.json())
  .then(data => setProducts(data))
}, [])
const [products, setProducts] = useState<Product[]>([])
  return (
  <div>
    <h1>Retail Intelligence Platform</h1>

    {products.map(product => (
      <p key={product.id}>
        {product.name} - ₹{product.price} - Stock: {product.stock}
      </p>
    ))}
  </div>
)
}

export default App
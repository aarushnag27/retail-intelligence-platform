import { useEffect, useState } from "react";
import "./RetailPages.css";

type InventoryItem = {
  id: number;
  name: string;
  stock: number;
  status: string;
};

function StaffPage() {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
useEffect(() => {
  fetch("http://localhost:8000/inventory")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch inventory");
      }
      return response.json();
    })
    .then((data) => {
      setInventory(data);
      setLoading(false);
    })
    .catch((error) => {
      setError(error.message);
      setLoading(false);
    });
}, []);
 return (
  <main className="retail-page staff-page">
    <header className="retail-header">
      <p className="retail-eyebrow">Store operations</p>
      <h1>Staff Dashboard</h1>
      <p className="retail-description">Monitor inventory levels and product availability.</p>
    </header>

    {error && <p className="retail-message retail-message--error">{error}</p>}
    {loading && <p className="retail-message">Loading inventory...</p>}

    <section className="retail-card retail-inventory" aria-labelledby="inventory-heading">
      <div className="retail-section-heading">
        <h2 id="inventory-heading">Inventory</h2>
        <p className="retail-description">Current stock and status for each product.</p>
      </div>
      <div className="retail-table-scroll">
    <table className="retail-table" aria-labelledby="inventory-heading">
      <thead>
        <tr>
          <th scope="col">Product</th>
          <th scope="col">Stock</th>
          <th scope="col">Status</th>
        </tr>
      </thead>

      <tbody>
        {inventory.map((item) => (
          <tr key={item.id}>
            <td>{item.name}</td>
            <td className="retail-stock">{item.stock}</td>
            <td><span className="retail-status" data-status={item.status}>{item.status}</span></td>
          </tr>
        ))}
      </tbody>
    </table>
      </div>
    </section>
  </main>
);
}

export default StaffPage;

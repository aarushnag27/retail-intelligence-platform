import { useEffect, useState } from "react";

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
  <>
    <h1>Staff Dashboard</h1>

    {error && <p>{error}</p>}
    {loading && <p>Loading inventory...</p>}

    <table>
      <thead>
        <tr>
          <th>Product</th>
          <th>Stock</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>
        {inventory.map((item) => (
          <tr key={item.id}>
            <td>{item.name}</td>
            <td>{item.stock}</td>
            <td>{item.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </>
);
}

export default StaffPage;
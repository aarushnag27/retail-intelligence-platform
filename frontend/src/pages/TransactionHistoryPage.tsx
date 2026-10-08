import { useEffect, useState } from "react";
type TransactionItem = {
  product_name: string;
  quantity: number;
  price: number;
};

type Transaction = {
  transaction_id: number;
  total: number;
  sold_at: string;
  items: TransactionItem[];
};

function TransactionHistoryPage() {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);
    useEffect(() => {
  fetch("http://localhost:8000/transactions")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch transactions");
      }

      return response.json();
    })
    .then((data) => {
      setTransactions(data);
      setLoading(false);
    })
    .catch((error) => {
      console.error(error);
    setError("Failed to fetch transactions");
    setLoading(false);
    });
}, []);

   return (
  <>
    <h1>Transaction History</h1>
    {error && <p>{error}</p>}
    {loading && <p>Loading transactions...</p>}
    {!error&&(
    <table>
      <thead>
        <tr>
          <th>Transaction ID</th>
          <th>Date/Time</th>
          <th>Items</th>
          <th>Total</th>
        </tr>
      </thead>

      <tbody>
        {transactions.map((transaction) => (
          <tr key={transaction.transaction_id}>
            <td>{transaction.transaction_id}</td>
            <td>{transaction.sold_at}</td>
            <td>
              {transaction.items.map((item) => (
                <div key={item.product_name}>
                  {item.product_name} × {item.quantity}
                </div>
              ))}
            </td>
            <td>₹{transaction.total}</td>
          </tr>
        ))}
      </tbody>
    </table>
    )}
  </>
);
}

export default TransactionHistoryPage;  
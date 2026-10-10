import { BrowserRouter, Route, Routes } from "react-router-dom"
import CustomerPage from "./pages/CustomerPage"
import StaffPage from "./pages/StaffPage"
import TransactionHistoryPage from "./pages/TransactionHistoryPage"
import SalesAnalyticsPage from "./pages/SalesAnalyticsPage"
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CustomerPage />} />
        <Route path="/staff" element={<StaffPage />} />
        <Route path="/staff/transactions" element={<TransactionHistoryPage />} />
        <Route path="/staff/analytics" element={<SalesAnalyticsPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

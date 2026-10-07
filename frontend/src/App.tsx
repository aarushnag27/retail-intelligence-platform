import { BrowserRouter, Route, Routes } from "react-router-dom"
import CustomerPage from "./pages/CustomerPage"
import StaffPage from "./pages/StaffPage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CustomerPage />} />
        <Route path="/staff" element={<StaffPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

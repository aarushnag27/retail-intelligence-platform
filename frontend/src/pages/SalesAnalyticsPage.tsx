import { useEffect, useState } from "react";
import AnalyticsOverview from "./AnalyticsOverview";
import TopProducts from "./TopProducts";
import HourlySalesChart from "./HourlySalesChart";
import DailySalesChart from "./DailySalesChart";
type TopProduct = {
  product_id: number;
  product_name: string;
  units_sold: number;
};

type HourlySale = {
  hour: number;
  revenue: number;
};

type DailySale = {
  date: string;
  revenue: number;
};

type SalesAnalytics = {
  total_revenue: number;
  total_transactions: number;
  total_units_sold: number;
  top_products: TopProduct[];
  hourly_sales: HourlySale[];
  daily_sales: DailySale[];
};

function SalesAnalyticsPage() {
  const [analytics, setAnalytics] = useState<SalesAnalytics | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/analytics/sales")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch sales analytics");
        }

        return response.json();
      })
      .then((data) => {
        setAnalytics(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
  return <p>Loading analytics...</p>;
}

if (error) {
  return <p>Error: {error}</p>;
}
if (!analytics) {
  return null;
}


 return (
  <>
    <h1>Sales Analytics</h1>

    <AnalyticsOverview
      total_revenue={analytics.total_revenue}
      total_transactions={analytics.total_transactions}
      total_units_sold={analytics.total_units_sold}
    />

    <TopProducts products={analytics.top_products} />
    <HourlySalesChart sales={analytics.hourly_sales} />
    <DailySalesChart sales={analytics.daily_sales} />
  </>
);
}

export default SalesAnalyticsPage;



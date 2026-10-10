type AnalyticsOverviewProps = {
  total_revenue: number;
  total_transactions: number;
  total_units_sold: number;
};

function AnalyticsOverview({
  total_revenue,
  total_transactions,
  total_units_sold,
}: AnalyticsOverviewProps) {
  return (
    <div>
      <div>
        <h3>Total Revenue</h3>
        <p>₹{total_revenue}</p>
      </div>

      <div>
        <h3>Total Transactions</h3>
        <p>{total_transactions}</p>
      </div>
        
      <div>
        <h3>Total Units Sold</h3>
        <p>{total_units_sold}</p>
      </div>
    </div>
  );
}

export default AnalyticsOverview;
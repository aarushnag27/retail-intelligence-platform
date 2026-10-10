import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";


type DailySale = {
  date: string;
  revenue: number;
};

type DailySalesChartProps = {
  sales: DailySale[];
};

function DailySalesChart({ sales }: DailySalesChartProps) {
  return (
    <div className="analytics-card analytics-chart analytics-daily">
      <h2>Sales by Day</h2>
      <p className="analytics-card-description">Daily revenue trends</p>
      <div className="analytics-chart-frame">
      <ResponsiveContainer width="100%" height={300}>
      <LineChart data={sales}>
      <XAxis dataKey="date" />
      <YAxis />
      <CartesianGrid strokeDasharray="3 3" />
      <Tooltip />
      <Line type="monotone" dataKey="revenue" />
      </LineChart>
      </ResponsiveContainer>
      </div>
      </div>
  );
}
export default DailySalesChart;

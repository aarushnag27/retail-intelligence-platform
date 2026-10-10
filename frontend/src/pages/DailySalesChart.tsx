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
    <div>
      <h2>Sales by Day</h2>
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
  );
}
export default DailySalesChart;
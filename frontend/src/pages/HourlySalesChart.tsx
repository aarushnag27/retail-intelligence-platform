import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} 
from "recharts";


type HourlySale = {
  hour: number;
  revenue: number;
};

type HourlySalesChartProps = {
  sales: HourlySale[];
};

function HourlySalesChart({ sales }: HourlySalesChartProps) {
    return (
  <div>
    <h2>Sales by Hour</h2>
    <ResponsiveContainer width="100%" height={300}>
    <LineChart data={sales}>
    <XAxis dataKey="hour" />
    <YAxis />
    <CartesianGrid strokeDasharray="3 3" />
    <Tooltip />
    <Line type="monotone" dataKey="revenue" />
    </LineChart>
    </ResponsiveContainer>
    
    </div>
    );
    }
    export default HourlySalesChart;
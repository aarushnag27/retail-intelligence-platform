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
  <div className="analytics-card analytics-chart analytics-hourly">
    <h2>Sales by Hour</h2>
    <p className="analytics-card-description">Revenue across the hours of the day</p>
    <div className="analytics-chart-frame">
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
    
    </div>
    );
    }
    export default HourlySalesChart;

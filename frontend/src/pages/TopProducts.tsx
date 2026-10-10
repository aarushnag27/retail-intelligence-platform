type TopProduct = {
  product_id: number;
  product_name: string;
  units_sold: number;
};

type TopProductsProps = {
  products: TopProduct[];
};

function TopProducts({ products }: TopProductsProps) {
 return (
  <div className="analytics-card analytics-products">
    <h2>Top Products</h2>
    <p className="analytics-card-description">Best sellers by units sold</p>

    <div className="analytics-product-list">
    {products.map((product) => (
      <div className="analytics-product-row" key={product.product_id}>
        <p>{product.product_name}</p>
        <p>{product.units_sold} units sold</p>
      </div>
    ))}
    </div>
  </div>
);
}
export default TopProducts;

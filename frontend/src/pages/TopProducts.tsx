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
  <div>
    <h2>Top Products</h2>

    {products.map((product) => (
      <div key={product.product_id}>
        <p>{product.product_name}</p>
        <p>{product.units_sold} units sold</p>
      </div>
    ))}
  </div>
);
}
export default TopProducts;
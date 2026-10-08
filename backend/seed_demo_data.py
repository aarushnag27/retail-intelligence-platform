"""SYNTHETIC DEMO DATA ONLY — never represent these sales as real store data.

Run from the project root (with the backend virtual environment activated):
    python backend/seed_demo_data.py                     # offline preview, no DB access
    python backend/seed_demo_data.py --write             # insert into configured dev DB
    python backend/seed_demo_data.py --write --seed 42 --days 30

Uses database.SessionLocal and the existing models; the schema must already exist.
No deletions, schema changes, checkout calls, predictions, or analytics are made.
Existing products retain their price, barcode, and stock. Historical sales assume
regular replenishment; stock is a present-day snapshot, not a simulated ledger.
New products use reserved DEMO-* barcodes and illustrative INR unit prices.
Categories are catalog metadata only because Product has no category column.
Repeated writes append another dataset; the warning and --write are intentional.
Use a development/test database, never a production database.
"""

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from decimal import Decimal
import math
import random


@dataclass(frozen=True)
class CatalogEntry:
    name: str
    category: str
    price: str
    stock: int
    demand: float
    profile: str


CATALOG = (
    CatalogEntry("Coca Cola", "Soft Drink", "40.00", 240, 10, "soda_night"),
    CatalogEntry("Pepsi", "Soft Drink", "40.00", 220, 9, "soda_night"),
    CatalogEntry("Sprite", "Soft Drink", "40.00", 180, 7, "soda"),
    CatalogEntry("Fanta", "Soft Drink", "40.00", 140, 5, "soda"),
    CatalogEntry("Bisleri Water", "Beverage", "20.00", 300, 10, "steady"),
    CatalogEntry("Sting Energy Drink", "Beverage", "20.00", 180, 7, "soda"),
    CatalogEntry("Mogu Mogu", "Beverage", "80.00", 45, 1, "occasional"),
    CatalogEntry("Lays Classic", "Snacks", "20.00", 240, 10, "evening_night"),
    CatalogEntry("Kurkure", "Snacks", "20.00", 180, 7, "evening"),
    CatalogEntry("Bingo Mad Angles", "Snacks", "20.00", 140, 5, "evening"),
    CatalogEntry("Haldiram's Bhujia", "Snacks", "50.00", 120, 5, "evening"),
    CatalogEntry("Oreo", "Biscuits", "30.00", 140, 5, "steady"),
    CatalogEntry("Parle-G", "Biscuits", "10.00", 200, 5, "steady"),
    CatalogEntry("Hide & Seek", "Biscuits", "30.00", 100, 3, "steady"),
    CatalogEntry("Maggi", "Instant Food", "15.00", 200, 7, "evening_night"),
    CatalogEntry("Yippee Noodles", "Instant Food", "15.00", 140, 5, "evening_night"),
    CatalogEntry("Dairy Milk", "Chocolate", "40.00", 180, 7, "evening"),
    CatalogEntry("KitKat", "Chocolate", "25.00", 140, 5, "evening"),
    CatalogEntry("5 Star", "Chocolate", "20.00", 140, 5, "evening"),
    CatalogEntry("Amul Ice Cream Cup", "Ice Cream", "40.00", 100, 5, "ice_cream"),
    CatalogEntry("Cornetto", "Ice Cream", "60.00", 80, 5, "ice_cream"),
    CatalogEntry("Amul Buttermilk", "Beverage", "15.00", 120, 5, "afternoon"),
    CatalogEntry("Red Bull", "Energy Drink", "125.00", 60, 2.5, "soda"),
    CatalogEntry("Paper Boat Juice", "Beverage", "30.00", 70, 2, "occasional"),
    CatalogEntry("Cup Noodles", "Instant Food", "55.00", 70, 2.5, "night"),
)

# Store traffic and product preferences are separate: peak traffic brings more
# baskets, while these relative weights change the composition of each basket.
# Columns: morning, afternoon, evening, 20:00–22:30, declining late night.
PROFILE_WEIGHTS = {
    "steady": (1, 1, 1, 1, 1),
    "soda_night": (0.5, 1.4, 1.5, 1.5, 0.9),
    "soda": (0.5, 1.5, 1.5, 0.9, 0.6),
    "occasional": (0.8, 1, 1, 0.8, 0.5),
    "evening": (0.5, 0.8, 1.8, 1.1, 0.7),
    "evening_night": (0.4, 0.7, 1.5, 1.8, 1.1),
    "ice_cream": (0.15, 0.25, 0.4, 3.5, 1.4),
    "afternoon": (0.7, 2, 0.8, 0.4, 0.2),
    "night": (0.3, 0.5, 0.9, 2, 1.5),
}


@dataclass(frozen=True)
class SaleItem:
    name: str
    quantity: int
    price: Decimal


@dataclass(frozen=True)
class Sale:
    sold_at: datetime
    items: tuple[SaleItem, ...]

    @property
    def total(self):
        return sum((item.price * item.quantity for item in self.items), Decimal("0.00"))


def time_band(hour):
    if hour < 12:
        return 0
    if hour < 17:
        return 1
    if hour < 20:
        return 2
    if hour < 22.5:
        return 3
    return 4


def poisson(rng, expected):
    """Draw a random arrival count for a short interval (no numpy needed)."""
    threshold = math.exp(-expected)
    count, probability = 0, 1.0
    while probability > threshold:
        count += 1
        probability *= rng.random()
    return count - 1


def generate_sales(prices, start_date, days=30, seed=None):
    """Generate random baskets, using supplied current prices and local naive time.

    The existing DateTime column and checkout both use naive local timestamps.
    Each day has store-wide noise, independent product noise, a weekend uplift,
    and occasional product spikes. Poisson arrivals avoid fixed daily counts.
    Weighted selection without replacement gives 1–4 distinct basket products.
    """
    rng = random.Random(seed)
    sales = []
    for offset in range(days):
        day = start_date + timedelta(days=offset)
        traffic = rng.lognormvariate(0, 0.22) * (1.15 if day.weekday() >= 5 else 1)
        demand = [entry.demand * rng.lognormvariate(0, 0.3) for entry in CATALOG]
        if rng.random() < 0.25:
            demand[rng.randrange(len(CATALOG))] *= rng.uniform(2, 4)

        # Open 08:00–24:00. Half-hour intervals isolate the 22:30 decline.
        for slot in range(32):
            hour = 8 + slot / 2
            band = time_band(hour)
            arrivals_per_hour = (3, 5, 8, 13, 4)[band]
            if hour >= 23:
                arrivals_per_hour = 2
            count = poisson(rng, arrivals_per_hour * 0.5 * traffic)
            weights = [demand[i] * PROFILE_WEIGHTS[entry.profile][band]
                       for i, entry in enumerate(CATALOG)]
            for _ in range(count):
                basket_size = rng.choices((1, 2, 3, 4), (0.35, 0.4, 0.2, 0.05))[0]
                available = list(range(len(CATALOG)))
                items = []
                for _ in range(basket_size):
                    selected = rng.choices(available, [weights[i] for i in available])[0]
                    available.remove(selected)
                    name = CATALOG[selected].name
                    quantity = rng.choices((1, 2, 3), (0.85, 0.13, 0.02))[0]
                    items.append(SaleItem(name, quantity, prices[name]))
                sold_at = datetime.combine(day, time(8)) + timedelta(
                    minutes=slot * 30, seconds=rng.randrange(1800))
                sales.append(Sale(sold_at, tuple(items)))
    return sorted(sales, key=lambda sale: sale.sold_at)


def ensure_products(db):
    """Reuse exact names or reserved barcodes, failing on ambiguous matches."""
    from sqlalchemy import or_, select
    from models import Product

    products, created = {}, 0
    for index, entry in enumerate(CATALOG, start=1):
        barcode = f"DEMO-{index:03d}"
        matches = list(db.scalars(select(Product).where(
            or_(Product.name == entry.name, Product.barcode == barcode))))
        if len(matches) > 1 or (matches and matches[0].name != entry.name):
            raise ValueError(f"Ambiguous name or demo barcode for {entry.name!r}; no data committed.")
        if matches:
            product = matches[0]
        else:
            product = Product(name=entry.name, barcode=barcode,
                              price=Decimal(entry.price), stock=entry.stock)
            db.add(product)
            created += 1
        if product.price is None or Decimal(str(product.price)) <= 0:
            raise ValueError(f"Invalid current price for {entry.name!r}; no data committed.")
        products[entry.name] = product
    db.flush()
    return products, created


def persist_sales(db, products, sales):
    from models import Transaction, TransactionItem

    for sale in sales:
        transaction = Transaction(total=sale.total, sold_at=sale.sold_at)
        db.add(transaction)
        db.flush()  # obtain the real primary key for the foreign-key item rows
        db.add_all([
            TransactionItem(transaction_id=transaction.transaction_id,
                            product_id=products[item.name].id,
                            quantity=item.quantity, price=item.price)
            for item in sale.items
        ])
    db.flush()


def print_summary(sales, start_date, days, created=None):
    print("SYNTHETIC DEMO DATA — not real store data")
    print(f"Period: {start_date} through {start_date + timedelta(days=days - 1)} (local time)")
    if created is None:
        print(f"Offline preview: {len(CATALOG)} catalog products; illustrative catalog prices")
        print("Nothing written. Pass --write to insert into your configured development database.")
    else:
        print(f"Products created: {created}; reused: {len(CATALOG) - created}")
    print(f"Transactions {'created' if created is not None else 'planned'}: {len(sales)}")
    print(f"Transaction items: {sum(len(sale.items) for sale in sales)}")
    print(f"Total sales value (INR): {sum((sale.total for sale in sales), Decimal('0.00')):.2f}")
    units = Counter()
    for sale in sales:
        for item in sale.items:
            units[item.name] += item.quantity
    print("Units by product:")
    for entry in CATALOG:
        print(f"  {entry.name}: {units[entry.name]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true", help="Append synthetic rows to the configured dev/test DB")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--start-date", type=date.fromisoformat, help="First day, YYYY-MM-DD; defaults to 30 days before today")
    parser.add_argument("--seed", type=int, help="Optional reproducible random seed")
    args = parser.parse_args()
    if not 1 <= args.days <= 366:
        parser.error("--days must be between 1 and 366")
    start_date = args.start_date or date.today() - timedelta(days=args.days)
    if start_date + timedelta(days=args.days) > date.today():
        parser.error("The sales period must contain only completed days (before today)")

    if args.write:
        from database import SessionLocal

        print("WARNING: appending SYNTHETIC DEMO DATA to the configured database.")
        print("Repeated runs append more sales; existing stock and records are preserved.")
        # Products and all sales commit together; any error rolls back everything.
        with SessionLocal.begin() as db:
            products, created = ensure_products(db)
            prices = {name: Decimal(str(product.price)) for name, product in products.items()}
            sales = generate_sales(prices, start_date, args.days, args.seed)
            persist_sales(db, products, sales)
        print_summary(sales, start_date, args.days, created)
    else:
        prices = {entry.name: Decimal(entry.price) for entry in CATALOG}
        sales = generate_sales(prices, start_date, args.days, args.seed)
        print_summary(sales, start_date, args.days)


if __name__ == "__main__":
    main()

"""
Seed data script — populates the database with sample entities.

Run automatically on first startup (when the DB is empty) so the API
is immediately usable without manual data entry.

Seed data mirrors the assignment document examples and adds additional
entities for richer testing.
"""

from sqlalchemy.orm import Session
from models import Customer, Seller, Product, Warehouse


def seed_database(db: Session) -> None:
    """
    Insert seed data if the database is empty.
    Skips seeding if any customers already exist (idempotent).
    """
    # Guard: skip if data already exists
    if db.query(Customer).first() is not None:
        return

    # -----------------------------------------------------------------------
    # Customers (Kirana stores)
    # -----------------------------------------------------------------------
    customers = [
        Customer(
            name="Shree Kirana Store",
            phone="9847******",
            email="shree.kirana@example.com",
            address="MG Road, Hyderabad",
            city="Hyderabad",
            pincode="500001",
            latitude=11.232,
            longitude=23.445495,
        ),
        Customer(
            name="Andheri Mini Mart",
            phone="9101******",
            email="andheri.mart@example.com",
            address="Andheri West, Mumbai",
            city="Mumbai",
            pincode="400058",
            latitude=17.232,
            longitude=33.445495,
        ),
        Customer(
            name="Rajesh General Store",
            phone="9876543210",
            email="rajesh.store@example.com",
            address="Koramangala, Bangalore",
            city="Bangalore",
            pincode="560034",
            latitude=12.9352,
            longitude=77.6245,
        ),
    ]

    # -----------------------------------------------------------------------
    # Sellers (product suppliers)
    # -----------------------------------------------------------------------
    sellers = [
        Seller(
            name="Nestle Seller",
            email="nestle.seller@example.com",
            phone="9800000001",
            address="Whitefield, Bangalore",
            city="Bangalore",
            latitude=12.9716,
            longitude=77.5946,
        ),
        Seller(
            name="Rice Seller",
            email="rice.seller@example.com",
            phone="9800000002",
            address="Balanagar, Hyderabad",
            city="Hyderabad",
            latitude=18.5204,
            longitude=73.8567,
        ),
        Seller(
            name="Sugar Seller",
            email="sugar.seller@example.com",
            phone="9800000003",
            address="Vashi, Navi Mumbai",
            city="Mumbai",
            latitude=19.0760,
            longitude=72.8777,
        ),
    ]

    # -----------------------------------------------------------------------
    # Products
    # -----------------------------------------------------------------------
    products = [
        Product(
            name="Maggie 500g Packet",
            seller_id=1,         # Nestle Seller
            weight_kg=0.5,
            length_cm=10.0,
            width_cm=10.0,
            height_cm=10.0,
            price=10.0,
            category="Instant Food",
            sku="NEST-MAG-500",
        ),
        Product(
            name="Rice Bag 10Kg",
            seller_id=2,         # Rice Seller
            weight_kg=10.0,
            length_cm=1000.0,
            width_cm=800.0,
            height_cm=500.0,
            price=500.0,
            category="Grains",
            sku="RICE-BAG-10K",
        ),
        Product(
            name="Sugar Bag 25Kg",
            seller_id=3,         # Sugar Seller
            weight_kg=25.0,
            length_cm=1000.0,
            width_cm=900.0,
            height_cm=600.0,
            price=700.0,
            category="Essentials",
            sku="SUGR-BAG-25K",
        ),
    ]

    # -----------------------------------------------------------------------
    # Warehouses
    # -----------------------------------------------------------------------
    warehouses = [
        Warehouse(
            name="BLR_Warehouse",
            address="Electronic City, Bangalore",
            city="Bangalore",
            pincode="560100",
            latitude=12.99999,
            longitude=37.923273,
        ),
        Warehouse(
            name="MUMB_Warehouse",
            address="Bhiwandi, Mumbai",
            city="Mumbai",
            pincode="421302",
            latitude=11.99999,
            longitude=27.923273,
        ),
    ]

    # -----------------------------------------------------------------------
    # Commit all seed data in a single transaction
    # -----------------------------------------------------------------------
    db.add_all(customers + sellers + products + warehouses)
    db.commit()
    print("✅ Database seeded with sample data.")

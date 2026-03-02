"""
SQLAlchemy ORM models for the B2B Shipping Charge Estimator.

Entities:
- Customer: Kirana stores that order products
- Seller: suppliers who list and sell products
- Product: items sold by sellers
- Warehouse: fulfillment centers that store and ship products

Following the assignment guideline: "do not limit yourself to the attributes given
for the entities and be creative in identifying more by taking inspiration from
e-commerce."
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Customer(Base):
    """
    Customer entity — represents a Kirana store that receives shipped products.
    Stores complete customer details including location for distance calculation.
    """

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(50), nullable=True)
    pincode = Column(String(10), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}')>"


class Seller(Base):
    """
    Seller entity — suppliers who list products on the marketplace.
    Sellers are located anywhere in India and ship to the nearest warehouse.
    """

    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(15), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(50), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Relationship: a seller can have many products
    products = relationship("Product", back_populates="seller")

    def __repr__(self):
        return f"<Seller(id={self.id}, name='{self.name}')>"


class Product(Base):
    """
    Product entity — items sold by sellers with weight and dimensions.
    Weight is critical for shipping charge calculation.
    Dimensions follow the assignment format (e.g., 10cm×10cm×10cm).
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    weight_kg = Column(Float, nullable=False)
    length_cm = Column(Float, nullable=False)
    width_cm = Column(Float, nullable=False)
    height_cm = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=True)
    sku = Column(String(50), nullable=True, unique=True)

    # Relationship back to seller
    seller = relationship("Seller", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', weight={self.weight_kg}kg)>"


class Warehouse(Base):
    """
    Warehouse entity — fulfillment centers that store and ship products.
    Located strategically across the country for efficient delivery.
    """

    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=True)
    city = Column(String(50), nullable=True)
    pincode = Column(String(10), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Warehouse(id={self.id}, name='{self.name}')>"

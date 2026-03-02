"""
Shipping service — business logic for shipping charge calculations.

Calculates the shipping charge based on:
1. Distance between warehouse and customer (Haversine)
2. Product weight
3. Transport mode (determined by distance)
4. Delivery speed (standard / express)

Transport Modes & Rates:
  - MiniVan  :   0–100 km  → ₹3 per km per kg
  - Truck    : 100–500 km  → ₹2 per km per kg
  - Aeroplane: 500+ km     → ₹1 per km per kg

Delivery Speed Surcharges:
  - Standard : FinalCharge = 10 + ShippingCharge
  - Express  : FinalCharge = 10 + ShippingCharge + (1.2 × weightKg)
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Warehouse, Customer, Product
from utils.distance import haversine_distance
from schemas import DeliverySpeed


# ---------------------------------------------------------------------------
# Transport mode configuration (rate in ₹ per km per kg)
# ---------------------------------------------------------------------------
TRANSPORT_MODES = [
    {"name": "MiniVan",   "max_distance": 100,  "rate": 3.0},
    {"name": "Truck",     "max_distance": 500,  "rate": 2.0},
    {"name": "Aeroplane", "max_distance": float("inf"), "rate": 1.0},
]

# Base charge added to every shipment
BASE_CHARGE = 10.0

# Express delivery surcharge multiplier per kg
EXPRESS_WEIGHT_SURCHARGE = 1.2


def _select_transport_mode(distance_km: float) -> dict:
    """
    Select the appropriate transport mode based on distance.

    Args:
        distance_km: Distance in kilometres.

    Returns:
        Transport mode dict with name, max_distance, and rate.
    """
    for mode in TRANSPORT_MODES:
        if distance_km <= mode["max_distance"]:
            return mode
    # Fallback (should never reach here)
    return TRANSPORT_MODES[-1]


def calculate_shipping_charge(
    warehouse_id: int,
    customer_id: int,
    product_id: int,
    delivery_speed: DeliverySpeed,
    db: Session,
) -> float:
    """
    Calculate the shipping charge for delivering a product from a warehouse
    to a customer.

    Args:
        warehouse_id: ID of the source warehouse.
        customer_id: ID of the destination customer.
        product_id: ID of the product being shipped.
        delivery_speed: 'standard' or 'express'.
        db: Active database session.

    Returns:
        Final shipping charge in Rs (rounded to 2 decimal places).

    Raises:
        HTTPException 404: If warehouse / customer / product is not found.
    """
    # --- Validate entities exist ---
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with id {warehouse_id} not found.",
        )

    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {customer_id} not found.",
        )

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )

    # --- Step 1: Calculate distance (Haversine) ---
    distance_km = haversine_distance(
        warehouse.latitude, warehouse.longitude,
        customer.latitude, customer.longitude,
    )

    # --- Step 2: Select transport mode ---
    transport = _select_transport_mode(distance_km)

    # --- Step 3: Base shipping charge = rate × distance × weight ---
    weight_kg = product.weight_kg
    shipping_charge = transport["rate"] * distance_km * weight_kg

    # --- Step 4: Apply delivery speed surcharge ---
    if delivery_speed == DeliverySpeed.STANDARD:
        final_charge = BASE_CHARGE + shipping_charge
    else:  # express
        final_charge = BASE_CHARGE + shipping_charge + (EXPRESS_WEIGHT_SURCHARGE * weight_kg)

    return round(final_charge, 2)

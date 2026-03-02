"""
Shipping API router.

Provides endpoints for shipping charge calculations:
1. GET  /shipping-charge           — calculate charge given a warehouse, customer, product, and speed.
2. POST /shipping-charge/calculate — combined: find nearest warehouse + calculate charge.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import (
    DeliverySpeed,
    ShippingChargeResponse,
    CombinedShippingRequest,
    CombinedShippingResponse,
)
from services.shipping_service import calculate_shipping_charge
from services.warehouse_service import get_nearest_warehouse

router = APIRouter(
    prefix="/api/v1/shipping-charge",
    tags=["Shipping"],
)


@router.get(
    "",
    response_model=ShippingChargeResponse,
    summary="Get Shipping Charge",
    description=(
        "Calculate shipping charge for a product from a specific warehouse "
        "to a customer with the chosen delivery speed."
    ),
)
def get_shipping_charge(
    warehouseId: int = Query(..., description="ID of the warehouse", ge=1),
    customerId: int = Query(..., description="ID of the customer", ge=1),
    productId: int = Query(..., description="ID of the product", ge=1),
    deliverySpeed: DeliverySpeed = Query(..., description="Delivery speed: 'standard' or 'express'"),
    db: Session = Depends(get_db),
):
    """
    Compute the shipping charge from a warehouse to a customer.

    Steps:
    1. Look up the warehouse, customer, and product.
    2. Calculate distance (Haversine).
    3. Select transport mode by distance.
    4. Apply delivery speed surcharge.
    """
    charge = calculate_shipping_charge(
        warehouse_id=warehouseId,
        customer_id=customerId,
        product_id=productId,
        delivery_speed=deliverySpeed,
        db=db,
    )
    return {"shippingCharge": charge}


@router.post(
    "/calculate",
    response_model=CombinedShippingResponse,
    summary="Combined: Nearest Warehouse + Shipping Charge",
    description=(
        "Finds the nearest warehouse to the seller, then calculates "
        "the shipping charge from that warehouse to the customer."
    ),
)
def calculate_combined_shipping(
    request: CombinedShippingRequest,
    db: Session = Depends(get_db),
):
    """
    Combined endpoint that:
    1. Finds the nearest warehouse to the seller.
    2. Calculates the shipping charge from that warehouse to the customer.
    3. Returns both results in a single response.
    """
    # Step 1: Find nearest warehouse
    nearest = get_nearest_warehouse(seller_id=request.sellerId, db=db)

    # Step 2: Calculate shipping charge from that warehouse
    charge = calculate_shipping_charge(
        warehouse_id=nearest["warehouseId"],
        customer_id=request.customerId,
        product_id=request.productId,
        delivery_speed=request.deliverySpeed,
        db=db,
    )

    return {
        "shippingCharge": charge,
        "nearestWarehouse": nearest,
    }

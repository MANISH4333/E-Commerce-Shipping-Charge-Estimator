"""
Warehouse service — business logic for warehouse operations.

Provides functionality to find the nearest warehouse to a given seller
using Haversine distance calculation.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Seller, Warehouse
from utils.distance import haversine_distance


def get_nearest_warehouse(seller_id: int, db: Session) -> dict:
    """
    Find the nearest warehouse to a seller's location.

    Args:
        seller_id: ID of the seller.
        db: Active database session.

    Returns:
        Dictionary with warehouseId and warehouseLocation (lat, lng).

    Raises:
        HTTPException 404: If the seller is not found.
        HTTPException 404: If no warehouses exist in the database.
    """
    # --- Validate seller exists ---
    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seller with id {seller_id} not found.",
        )

    # --- Fetch all warehouses ---
    warehouses = db.query(Warehouse).all()
    if not warehouses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No warehouses available in the system.",
        )

    # --- Calculate distances and find the nearest ---
    nearest_warehouse = None
    min_distance = float("inf")

    for warehouse in warehouses:
        distance = haversine_distance(
            seller.latitude, seller.longitude,
            warehouse.latitude, warehouse.longitude,
        )
        if distance < min_distance:
            min_distance = distance
            nearest_warehouse = warehouse

    return {
        "warehouseId": nearest_warehouse.id,
        "warehouseLocation": {
            "lat": round(nearest_warehouse.latitude, 5),
            "long": round(nearest_warehouse.longitude, 6),
        },
    }

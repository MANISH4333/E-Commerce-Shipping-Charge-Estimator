"""
Warehouse API router.

Provides endpoints for warehouse-related operations such as
finding the nearest warehouse to a seller.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import NearestWarehouseResponse
from services.warehouse_service import get_nearest_warehouse

router = APIRouter(
    prefix="/api/v1/warehouse",
    tags=["Warehouse"],
)


@router.get(
    "/nearest",
    response_model=NearestWarehouseResponse,
    summary="Get Nearest Warehouse",
    description="Returns the nearest warehouse to a given seller's location.",
)
def nearest_warehouse(
    sellerId: int = Query(..., description="ID of the seller", ge=1),
    productId: int = Query(..., description="ID of the product", ge=1),
    db: Session = Depends(get_db),
):
    """
    Find the warehouse closest to the specified seller.

    - **sellerId**: ID of the seller whose location is used as reference.
    - **productId**: ID of the product (logged for traceability).
    """
    result = get_nearest_warehouse(seller_id=sellerId, db=db)
    return result

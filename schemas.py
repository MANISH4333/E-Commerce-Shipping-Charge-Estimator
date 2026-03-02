"""
Pydantic schemas for request validation and response serialization.

These schemas enforce data contracts between the API and clients,
ensuring type safety and automatic documentation in Swagger UI.
"""

from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DeliverySpeed(str, Enum):
    """Supported delivery speed options."""
    STANDARD = "standard"
    EXPRESS = "express"


class TransportMode(str, Enum):
    """Transport modes determined by distance."""
    MINIVAN = "MiniVan"
    TRUCK = "Truck"
    AEROPLANE = "Aeroplane"


# ---------------------------------------------------------------------------
# Response Schemas
# ---------------------------------------------------------------------------

class WarehouseLocation(BaseModel):
    """Geographic coordinates of a warehouse."""
    lat: float = Field(..., description="Latitude of the warehouse")
    long: float = Field(..., description="Longitude of the warehouse")


class NearestWarehouseResponse(BaseModel):
    """Response for the nearest warehouse lookup."""
    warehouseId: int = Field(..., description="ID of the nearest warehouse")
    warehouseLocation: WarehouseLocation


class ShippingChargeResponse(BaseModel):
    """Response for the shipping charge calculation."""
    shippingCharge: float = Field(..., description="Calculated shipping charge in Rs")


class CombinedShippingResponse(BaseModel):
    """Response for the combined nearest warehouse + shipping charge calculation."""
    shippingCharge: float = Field(..., description="Calculated shipping charge in Rs")
    nearestWarehouse: NearestWarehouseResponse


# ---------------------------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------------------------

class CombinedShippingRequest(BaseModel):
    """Request body for the combined shipping charge calculation endpoint."""
    sellerId: int = Field(..., description="ID of the seller")
    productId: int = Field(..., description="ID of the product")
    customerId: int = Field(..., description="ID of the customer")
    deliverySpeed: DeliverySpeed = Field(..., description="Delivery speed: 'standard' or 'express'")


# ---------------------------------------------------------------------------
# Error Schema
# ---------------------------------------------------------------------------

class ErrorResponse(BaseModel):
    """Standard error response body."""
    detail: str = Field(..., description="Human-readable error message")

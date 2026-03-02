# B2B E-Commerce Shipping Charge Estimator

A production-quality **FastAPI** backend for a B2B e-commerce marketplace that calculates shipping charges for Kirana stores.

## 🏗️ Architecture

```
project/
├── main.py                  # FastAPI app entry point
├── database.py              # SQLite + SQLAlchemy configuration
├── models.py                # ORM models (Customer, Seller, Product, Warehouse)
├── schemas.py               # Pydantic request/response schemas
├── seed_data.py             # Sample data for quick testing
├── requirements.txt         # Python dependencies
├── services/
│   ├── warehouse_service.py # Nearest warehouse logic
│   └── shipping_service.py  # Shipping charge calculation
├── utils/
│   └── distance.py          # Haversine distance formula
└── routers/
    ├── warehouse_router.py  # /api/v1/warehouse/* endpoints
    └── shipping_router.py   # /api/v1/shipping-charge/* endpoints
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
uvicorn main:app --reload
```

The server starts at **http://127.0.0.1:8000**. The database and seed data are created automatically on first run.

### 3. Explore the API

| Tool       | URL                              |
|------------|----------------------------------|
| Swagger UI | http://127.0.0.1:8000/docs       |
| ReDoc      | http://127.0.0.1:8000/redoc      |
| Health     | http://127.0.0.1:8000/           |

## 📡 API Endpoints

### 1. Get Nearest Warehouse

```
GET /api/v1/warehouse/nearest?sellerId=1&productId=1
```

**Response:**
```json
{
  "warehouseId": 1,
  "warehouseLocation": {
    "lat": 12.99999,
    "long": 37.923273
  }
}
```

### 2. Get Shipping Charge

```
GET /api/v1/shipping-charge?warehouseId=1&customerId=1&productId=1&deliverySpeed=standard
```

**Response:**
```json
{
  "shippingCharge": 150.00
}
```

### 3. Combined: Nearest Warehouse + Shipping Charge

```
POST /api/v1/shipping-charge/calculate
Content-Type: application/json

{
  "sellerId": 1,
  "productId": 1,
  "customerId": 1,
  "deliverySpeed": "express"
}
```

**Response:**
```json
{
  "shippingCharge": 180.00,
  "nearestWarehouse": {
    "warehouseId": 1,
    "warehouseLocation": {
      "lat": 12.99999,
      "long": 37.923273
    }
  }
}
```

## 💰 Shipping Charge Logic

### Transport Modes

| Mode      | Distance Range | Rate (₹/km/kg) |
|-----------|---------------|-----------------|
| MiniVan   | 0–100 km      | ₹3              |
| Truck     | 100–500 km    | ₹2              |
| Aeroplane | 500+ km       | ₹1              |

### Delivery Speed

| Speed    | Formula                                   |
|----------|-------------------------------------------|
| Standard | `FinalCharge = 10 + ShippingCharge`        |
| Express  | `FinalCharge = 10 + ShippingCharge + (1.2 × weightKg)` |

### Distance

Calculated using the **Haversine formula** (great-circle distance between two lat/lng points).

## 🗃️ Seed Data

The database is pre-loaded with:

| Entity     | Records                                              |
|------------|-----------------------------------------------------|
| Customers  | Shree Kirana Store, Andheri Mini Mart, Rajesh General Store |
| Sellers    | Nestle Seller, Rice Seller, Sugar Seller              |
| Products   | Maggie 500g (0.5 kg), Rice Bag (10 kg), Sugar Bag (25 kg) |
| Warehouses | BLR_Warehouse, MUMB_Warehouse                        |

## ⚠️ Error Handling

All errors return structured JSON:

```json
{
  "detail": "Customer with id 99 not found."
}
```

| Status Code | Scenario                    |
|------------|------------------------------|
| 404        | Entity not found             |
| 422        | Invalid / missing parameters |
| 500        | Internal server error        |

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** — high-performance async web framework
- **SQLAlchemy** — ORM for database operations
- **SQLite** — lightweight embedded database
- **Pydantic** — data validation and serialization
- **Uvicorn** — ASGI server

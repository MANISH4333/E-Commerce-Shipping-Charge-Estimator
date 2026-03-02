"""
B2B E-Commerce Shipping Charge Estimator — FastAPI Application

Entry point for the application. Handles:
  - FastAPI app creation with metadata for Swagger docs
  - Automatic database table creation on startup
  - Seed data insertion on first run
  - CORS middleware for frontend integration
  - Static file serving for the frontend
  - Router registration

Run with:
    uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from database import engine, Base, SessionLocal
from seed_data import seed_database
from routers import warehouse_router, shipping_router

# Path to the frontend directory
FRONTEND_DIR = Path(__file__).parent / "frontend"


# ---------------------------------------------------------------------------
#  Lifespan: startup / shutdown events
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    - Creates all database tables on startup.
    - Seeds the database with sample data if empty.
    """
    # --- Startup ---
    print("🚀 Creating database tables...")
    Base.metadata.create_all(bind=engine)

    # Seed data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    print("✅ Application ready!")
    yield  # App is running

    # --- Shutdown ---
    print("🛑 Shutting down...")


# ---------------------------------------------------------------------------
#  FastAPI App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="B2B Shipping Charge Estimator",
    description=(
        "REST API for a B2B e-commerce marketplace (Kirana stores). "
        "Calculates shipping charges based on distance, product weight, "
        "transport mode, and delivery speed."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc alternative
)


# ---------------------------------------------------------------------------
#  CORS Middleware — allows frontend to call this API
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
#  Global Exception Handler — catches unhandled errors gracefully
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Return a clean JSON error for any unhandled exception."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


# ---------------------------------------------------------------------------
#  Register API Routers
# ---------------------------------------------------------------------------
app.include_router(warehouse_router.router)
app.include_router(shipping_router.router)


# ---------------------------------------------------------------------------
#  Static Files (CSS, JS served from /static/)
# ---------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ---------------------------------------------------------------------------
#  Health Check API
# ---------------------------------------------------------------------------
@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint — confirms the API is running."""
    return {
        "status": "healthy",
        "service": "B2B Shipping Charge Estimator",
        "version": "1.0.0",
    }


# ---------------------------------------------------------------------------
#  Serve Frontend — root route returns the HTML page
# ---------------------------------------------------------------------------
@app.get("/", tags=["Frontend"], include_in_schema=False)
def serve_frontend():
    """Serve the main frontend HTML page."""
    return FileResponse(str(FRONTEND_DIR / "index.html"))

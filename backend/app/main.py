import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database import db_manager
from backend.app.routes import auth, telemetry, ingest

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Adaptive Lightweight Network Intrusion Detection System REST & Streaming API"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(telemetry.router, prefix=settings.API_V1_PREFIX)
app.include_router(ingest.router, prefix=settings.API_V1_PREFIX)
app.include_router(telemetry.router) # Allows /ws/telemetry without prefix too

@app.on_event("startup")
async def startup_event():
    await db_manager.connect_to_database()

@app.on_event("shutdown")
async def shutdown_event():
    await db_manager.close_database_connection()

@app.get("/")
async def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "mongodb" if db_manager.is_connected_to_mongo else "in-memory (resilient mode)",
        "features_selected": settings.SELECTED_FEATURE_COUNT
    }

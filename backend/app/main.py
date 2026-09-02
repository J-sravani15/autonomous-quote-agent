"""
Main FastAPI Application - Autonomous Quote Agent Intelligence Platform.

Configures the FastAPI server with:
- CORS middleware for frontend communication
- Multi-agent prediction pipeline
- Structured logging
- API routes

The application orchestrates four specialized AI agents that analyze
insurance quotes to predict conversion probability and recommend actions.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predict
from loguru import logger
import sys

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO",
)
logger.add(
    "logs/app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
    level="INFO",
    rotation="500 MB",
)

app = FastAPI(
    title="Autonomous Quote Agent API",
    description="Multi-agent AI system for insurance quote analysis and decision automation",
    version="2.0.0",
)

# CORS CONFIGURATION - Allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, tags=["Predictions"])


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "message": "Autonomous Quote Agent System v2.0.0 running",
        "status": "operational",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "quote-analysis",
        "version": "2.0.0",
    }

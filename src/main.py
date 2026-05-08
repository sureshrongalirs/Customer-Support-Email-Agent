"""FastAPI Application Entry Point"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.api.routes import router as api_router
from src.api.ui_routes import router as ui_router
from src.core.config import settings
from src.core.logger import setup_logger
from src.services.email_store import EmailStore

logger = setup_logger(__name__)
email_store = EmailStore()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Customer Support Email Agent API")
    yield
    logger.info("Shutting down Customer Support Email Agent API")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="An intelligent customer support email agent powered by LangGraph",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(api_router)
    app.include_router(ui_router)

    # Serve static files
    frontend_path = Path(__file__).parent.parent / "frontend"
    if frontend_path.exists():
        app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
        logger.info(f"Mounted static files from {frontend_path}")

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "Customer Support Email Agent"}

    @app.get("/")
    async def root():
        """Root endpoint - redirect to UI."""
        return FileResponse(frontend_path / "index.html") if frontend_path.exists() else {
            "message": "Welcome to Customer Support Email Agent API",
            "version": settings.api_version,
            "docs": "/docs",
            "ui": "/ui",
            "endpoints": {
                "process_email": "POST /api/v1/emails/process",
                "get_status": "GET /api/v1/emails/{email_id}",
                "get_details": "GET /api/v1/emails/{email_id}/details",
                "statistics": "GET /api/v1/stats",
                "inbox": "GET /inbox",
                "email_detail": "GET /inbox/{email_id}",
            },
        }

    @app.get("/ui")
    async def serve_ui():
        """Serve the UI."""
        if frontend_path.exists():
            return FileResponse(frontend_path / "index.html")
        raise Exception("Frontend files not found")

    @app.get("/favicon.ico")
    async def favicon():
        """Favicon endpoint."""
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.env == "development",
        log_level=settings.log_level.lower(),
    )

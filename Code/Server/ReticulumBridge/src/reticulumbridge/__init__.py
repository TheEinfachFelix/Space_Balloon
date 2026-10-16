from __future__ import annotations

from time import perf_counter

from fastapi import FastAPI
from loguru import logger
from reticulumbridge.api.health import router as health_router
from reticulumbridge.dependencies import get_settings
from reticulumbridge.utils.logging import setup_logging
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from .main import lifespan


def create_app() -> FastAPI:
    """Factory-Funktion zur Erstellung der FastAPI-Instanz."""
    app = FastAPI(
        title='ReticulumBridge',
        description='Zentrale Middleware um den Ballon zu verwalten',
        version='0.1.0',
        lifespan=lifespan,
    )

    # API-Router registrieren
    app.include_router(health_router, prefix='/api', tags=['Monitoring'])

    @app.middleware('http')
    async def log_http_request(
        request: Request, call_next: RequestResponseEndpoint,
    ) -> Response:
        started_at = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = (perf_counter() - started_at) * 1000
            logger.exception(
                'HTTP {} {} failed after {:.2f} ms',
                request.method,
                request.url.path,
                elapsed_ms,
            )
            raise

        elapsed_ms = (perf_counter() - started_at) * 1000
        log = logger.warning if response.status_code >= 400 else logger.info
        log(
            'HTTP {} {} -> {} in {:.2f} ms',
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response

    return app


# Globale App-Instanz für Uvicorn
app = create_app()


def main():
    """Einstiegspunkt für das Konsolenskript (definiert in pyproject.toml)."""
    import uvicorn

    settings = get_settings()
    setup_logging(settings)

    logger.info(
        f"Starte Uvicorn-Server auf {settings.reticulum_bridge.api.host}:"
        + f"{settings.reticulum_bridge.api.port}...",
    )
    uvicorn.run(
        'reticulumbridge:app',
        host=settings.reticulum_bridge.api.host,
        port=settings.reticulum_bridge.api.port,
        reload=True,
        log_config=None,
        log_level=None,
    )


if __name__ == '__main__':

    main()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import administracion, clientes, reportes, territorios, ventas
from utils.exceptions import AppError


def create_app() -> FastAPI:
    """Construye la aplicacion FastAPI y registra middleware, rutas y errores."""
    app = FastAPI(title="Backend AdventureWorks2025")

    # CORS permite que Blazor consuma la API desde su propio puerto local.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        """Devuelve errores controlados con un formato uniforme para el frontend."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.get("/")
    def inicio() -> dict[str, str]:
        """Endpoint simple para validar que el backend esta en ejecucion."""
        return {"mensaje": "Servidor Python conectado y corriendo"}

    app.include_router(clientes.router)
    app.include_router(reportes.router)
    app.include_router(administracion.usuarios_router)
    app.include_router(administracion.roles_router)
    app.include_router(territorios.router)
    app.include_router(ventas.router)
    return app


app = create_app()

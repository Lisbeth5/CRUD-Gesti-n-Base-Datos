from datetime import date

from fastapi import APIRouter, Query

from schemas.reportes import (
    DetalleVentaResponse,
    ResumenVentaResponse,
    VentaCategoriaResponse,
    VentaProductoResponse,
    VentaTerritorioResponse,
)
from services import reportes_service


router = APIRouter(prefix="/api/reportes", tags=["Reportes"])


@router.get("/detalle-ventas", response_model=list[DetalleVentaResponse])
def obtener_detalle_ventas(
    fecha_inicial: date | None = Query(default=None),
    fecha_final: date | None = Query(default=None),
    cliente_id: int | None = Query(default=None, ge=1),
    vendedor_id: int | None = Query(default=None, ge=1),
) -> list[DetalleVentaResponse]:
    """Endpoint del reporte de detalle de ventas con filtros opcionales."""
    return reportes_service.obtener_detalle_ventas(
        fecha_inicial,
        fecha_final,
        cliente_id,
        vendedor_id,
    )


@router.get("/resumen-ventas", response_model=list[ResumenVentaResponse])
def obtener_resumen_ventas(
    fecha_inicial: date | None = Query(default=None),
    fecha_final: date | None = Query(default=None),
    cliente_id: int | None = Query(default=None, ge=1),
    vendedor_id: int | None = Query(default=None, ge=1),
) -> list[ResumenVentaResponse]:
    """Endpoint del reporte de resumen de ventas con filtros opcionales."""
    return reportes_service.obtener_resumen_ventas(
        fecha_inicial,
        fecha_final,
        cliente_id,
        vendedor_id,
    )


@router.get("/productos", response_model=list[VentaProductoResponse])
def obtener_ventas_por_producto(
    fecha_inicial: date | None = Query(default=None),
    fecha_final: date | None = Query(default=None),
    producto_id: int | None = Query(default=None, ge=1),
) -> list[VentaProductoResponse]:
    """Endpoint del reporte de ventas por producto."""
    return reportes_service.obtener_ventas_por_producto(
        fecha_inicial,
        fecha_final,
        producto_id,
    )


@router.get("/categorias", response_model=list[VentaCategoriaResponse])
def obtener_ventas_por_categoria(
    fecha_inicial: date | None = Query(default=None),
    fecha_final: date | None = Query(default=None),
    categoria_id: int | None = Query(default=None, ge=1),
) -> list[VentaCategoriaResponse]:
    """Endpoint del reporte de ventas por categoria."""
    return reportes_service.obtener_ventas_por_categoria(
        fecha_inicial,
        fecha_final,
        categoria_id,
    )


@router.get("/territorios", response_model=list[VentaTerritorioResponse])
def obtener_ventas_por_territorio(
    fecha_inicial: date | None = Query(default=None),
    fecha_final: date | None = Query(default=None),
    territorio_id: int | None = Query(default=None, ge=1),
) -> list[VentaTerritorioResponse]:
    """Endpoint del reporte de ventas por territorio."""
    return reportes_service.obtener_ventas_por_territorio(
        fecha_inicial,
        fecha_final,
        territorio_id,
    )

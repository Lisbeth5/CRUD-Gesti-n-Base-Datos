from datetime import date

from typing import Literal

from fastapi import APIRouter, Query
from fastapi.responses import Response

from schemas.reportes import (
    DetalleVentaResponse,
    ResumenVentaResponse,
    VentaCategoriaResponse,
    VentaProductoResponse,
    VentaTerritorioResponse,
)
from services import reportes_pdf_service, reportes_service


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


@router.get("/exportar-pdf")
def exportar_reporte_pdf(
    tipo: Literal["detalle", "resumen", "productos", "categorias", "territorios"] = Query(default="detalle"),
    fecha_inicial: date | None = Query(default=None),
    fecha_final: date | None = Query(default=None),
    cliente_id: int | None = Query(default=None, ge=1),
    vendedor_id: int | None = Query(default=None, ge=1),
    producto_id: int | None = Query(default=None, ge=1),
    categoria_id: int | None = Query(default=None, ge=1),
    territorio_id: int | None = Query(default=None, ge=1),
) -> Response:
    """Descarga en PDF todas las filas del reporte consultado con sus filtros."""
    if tipo == "detalle":
        filas = reportes_service.obtener_detalle_ventas(fecha_inicial, fecha_final, cliente_id, vendedor_id)
        identificadores = {"ID Cliente": cliente_id, "ID Vendedor": vendedor_id}
    elif tipo == "resumen":
        filas = reportes_service.obtener_resumen_ventas(fecha_inicial, fecha_final, cliente_id, vendedor_id)
        identificadores = {"ID Cliente": cliente_id, "ID Vendedor": vendedor_id}
    elif tipo == "productos":
        filas = reportes_service.obtener_ventas_por_producto(fecha_inicial, fecha_final, producto_id)
        identificadores = {"ID Producto": producto_id}
    elif tipo == "categorias":
        filas = reportes_service.obtener_ventas_por_categoria(fecha_inicial, fecha_final, categoria_id)
        identificadores = {"ID Categoria": categoria_id}
    else:
        filas = reportes_service.obtener_ventas_por_territorio(fecha_inicial, fecha_final, territorio_id)
        identificadores = {"ID Territorio": territorio_id}

    contenido = reportes_pdf_service.generar_reporte_pdf(tipo, filas, fecha_inicial, fecha_final, identificadores)
    return Response(
        content=contenido,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="reporte_{tipo}.pdf"'},
    )

from datetime import date

from repositories import reportes_repository
from schemas.reportes import (
    DetalleVentaResponse,
    ResumenVentaResponse,
    VentaCategoriaResponse,
    VentaProductoResponse,
    VentaTerritorioResponse,
)
from utils.exceptions import AppError


def _validar_rango_fechas(fecha_inicial: date | None, fecha_final: date | None) -> None:
    """Valida que el rango de fechas sea coherente cuando ambas fechas existen."""
    if fecha_inicial and fecha_final and fecha_inicial > fecha_final:
        raise AppError("La fecha inicial no puede ser mayor que la fecha final.")


def obtener_detalle_ventas(
    fecha_inicial: date | None,
    fecha_final: date | None,
    cliente_id: int | None,
    vendedor_id: int | None,
) -> list[DetalleVentaResponse]:
    """Coordina el reporte detallado de ventas."""
    _validar_rango_fechas(fecha_inicial, fecha_final)
    filas = reportes_repository.obtener_detalle_ventas(
        fecha_inicial,
        fecha_final,
        cliente_id,
        vendedor_id,
    )
    return [DetalleVentaResponse.model_validate(fila) for fila in filas]


def obtener_resumen_ventas(
    fecha_inicial: date | None,
    fecha_final: date | None,
    cliente_id: int | None,
    vendedor_id: int | None,
) -> list[ResumenVentaResponse]:
    """Coordina el reporte resumido de ventas."""
    _validar_rango_fechas(fecha_inicial, fecha_final)
    filas = reportes_repository.obtener_resumen_ventas(
        fecha_inicial,
        fecha_final,
        cliente_id,
        vendedor_id,
    )
    return [ResumenVentaResponse.model_validate(fila) for fila in filas]


def obtener_ventas_por_producto(
    fecha_inicial: date | None,
    fecha_final: date | None,
    producto_id: int | None,
) -> list[VentaProductoResponse]:
    """Coordina el reporte de ventas por producto."""
    _validar_rango_fechas(fecha_inicial, fecha_final)
    filas = reportes_repository.obtener_ventas_por_producto(
        fecha_inicial,
        fecha_final,
        producto_id,
    )
    return [VentaProductoResponse.model_validate(fila) for fila in filas]


def obtener_ventas_por_categoria(
    fecha_inicial: date | None,
    fecha_final: date | None,
    categoria_id: int | None,
) -> list[VentaCategoriaResponse]:
    """Coordina el reporte de ventas por categoria."""
    _validar_rango_fechas(fecha_inicial, fecha_final)
    filas = reportes_repository.obtener_ventas_por_categoria(
        fecha_inicial,
        fecha_final,
        categoria_id,
    )
    return [VentaCategoriaResponse.model_validate(fila) for fila in filas]


def obtener_ventas_por_territorio(
    fecha_inicial: date | None,
    fecha_final: date | None,
    territorio_id: int | None,
) -> list[VentaTerritorioResponse]:
    """Coordina el reporte de ventas por territorio."""
    _validar_rango_fechas(fecha_inicial, fecha_final)
    filas = reportes_repository.obtener_ventas_por_territorio(
        fecha_inicial,
        fecha_final,
        territorio_id,
    )
    return [VentaTerritorioResponse.model_validate(fila) for fila in filas]

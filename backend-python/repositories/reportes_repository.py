from datetime import date
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.database import get_engine
from utils.exceptions import DatabaseError


def _ejecutar_reporte(nombre_procedimiento: str, parametros: dict[str, Any]) -> list[dict]:
    """Ejecuta un procedimiento almacenado de reportes y retorna filas como diccionarios."""
    try:
        placeholders = ", ".join(f":{nombre}" for nombre in parametros)
        sentencia = text(f"EXEC {nombre_procedimiento} {placeholders}")

        with get_engine().connect() as connection:
            result = connection.execute(sentencia, parametros)
            return [dict(row) for row in result.mappings().all()]
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al ejecutar {nombre_procedimiento}: {exc}") from exc


def obtener_detalle_ventas(
    fecha_inicial: date | None,
    fecha_final: date | None,
    cliente_id: int | None,
    vendedor_id: int | None,
) -> list[dict]:
    """Obtiene el detalle de ventas desde SQL Server."""
    return _ejecutar_reporte(
        "Sales.USP_ReporteDetalleVentas",
        {
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final,
            "cliente_id": cliente_id,
            "vendedor_id": vendedor_id,
        },
    )


def obtener_resumen_ventas(
    fecha_inicial: date | None,
    fecha_final: date | None,
    cliente_id: int | None,
    vendedor_id: int | None,
) -> list[dict]:
    """Obtiene el resumen de ventas desde SQL Server."""
    return _ejecutar_reporte(
        "Sales.USP_ReporteResumenVentas",
        {
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final,
            "cliente_id": cliente_id,
            "vendedor_id": vendedor_id,
        },
    )


def obtener_ventas_por_producto(
    fecha_inicial: date | None,
    fecha_final: date | None,
    producto_id: int | None,
) -> list[dict]:
    """Obtiene ventas agrupadas por producto desde SQL Server."""
    return _ejecutar_reporte(
        "Sales.USP_ReporteVentasPorProducto",
        {
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final,
            "producto_id": producto_id,
        },
    )


def obtener_ventas_por_categoria(
    fecha_inicial: date | None,
    fecha_final: date | None,
    categoria_id: int | None,
) -> list[dict]:
    """Obtiene ventas agrupadas por categoria desde SQL Server."""
    return _ejecutar_reporte(
        "Sales.USP_ReporteVentasPorCategoria",
        {
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final,
            "categoria_id": categoria_id,
        },
    )


def obtener_ventas_por_territorio(
    fecha_inicial: date | None,
    fecha_final: date | None,
    territorio_id: int | None,
) -> list[dict]:
    """Obtiene ventas por territorio, categoria y producto desde SQL Server."""
    return _ejecutar_reporte(
        "Sales.USP_ReporteVentasPorTerritorio",
        {
            "fecha_inicial": fecha_inicial,
            "fecha_final": fecha_final,
            "territorio_id": territorio_id,
        },
    )

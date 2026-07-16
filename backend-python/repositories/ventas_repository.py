from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.database import get_engine
from schemas.ventas import VentaCreateRequest, VentaDetalleCreateRequest, VentaDetalleUpdateRequest
from utils.exceptions import DatabaseError


def _ejecutar_listado(nombre_procedimiento: str, parametros: dict[str, Any]) -> list[dict]:
    """Ejecuta un procedimiento almacenado de consulta y devuelve diccionarios."""
    try:
        placeholders = ", ".join(f":{nombre}" for nombre in parametros)
        sentencia = text(f"EXEC {nombre_procedimiento} {placeholders}")

        with get_engine().connect() as connection:
            result = connection.execute(sentencia, parametros)
            return [dict(row) for row in result.mappings().all()]
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al ejecutar {nombre_procedimiento}: {exc}") from exc


def _ejecutar_comando(nombre_procedimiento: str, parametros: dict[str, Any]) -> None:
    """Ejecuta un procedimiento almacenado de escritura dentro de una transacción."""
    try:
        placeholders = ", ".join(f":{nombre}" for nombre in parametros)
        sentencia = text(f"EXEC {nombre_procedimiento} {placeholders}")

        with get_engine().begin() as connection:
            connection.execute(sentencia, parametros)
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al ejecutar {nombre_procedimiento}: {exc}") from exc


def _ejecutar_escalar(nombre_procedimiento: str, parametros: dict[str, Any]) -> dict | None:
    """Ejecuta un procedimiento almacenado que devuelve una sola fila."""
    try:
        placeholders = ", ".join(f":{nombre}" for nombre in parametros)
        sentencia = text(f"EXEC {nombre_procedimiento} {placeholders}")

        with get_engine().connect() as connection:
            result = connection.execute(sentencia, parametros)
            row = result.mappings().first()
            return dict(row) if row else None
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al ejecutar {nombre_procedimiento}: {exc}") from exc


def listar_ventas(venta_id: int | None, cliente_id: int | None, vendedor_id: int | None, fecha_desde: str | None, fecha_hasta: str | None) -> list[dict]:
    """Consulta cabeceras de venta."""
    return _ejecutar_listado(
        "dbo.USP_VentaListar",
        {
            "venta_id": venta_id,
            "cliente_id": cliente_id,
            "vendedor_id": vendedor_id,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
        },
    )


def obtener_venta(venta_id: int) -> dict | None:
    """Obtiene la cabecera y los detalles de una venta."""
    cabecera = _ejecutar_listado(
        "dbo.USP_VentaObtener",
        {"venta_id": venta_id},
    )
    if not cabecera:
        return None
    detalles = _ejecutar_listado(
        "dbo.USP_VentaDetalleListar",
        {"venta_id": venta_id},
    )
    return {"cabecera": cabecera[0], "detalles": detalles}


def crear_venta(venta: VentaCreateRequest) -> int:
    """Crea una venta nueva y devuelve su identificador."""
    row = _ejecutar_escalar(
        "dbo.USP_VentaCrear",
        {
            "cliente_id": venta.ClienteID,
            "vendedor_id": venta.VendedorID,
            "territorio_id": venta.TerritorioID,
            "observaciones": venta.Observaciones,
        },
    )
    if not row or "VentaID" not in row:
        raise DatabaseError("No se pudo crear la venta.")
    return int(row["VentaID"])


def actualizar_venta(venta_id: int, venta: VentaCreateRequest) -> None:
    """Actualiza la cabecera de una venta."""
    _ejecutar_comando(
        "dbo.USP_VentaActualizar",
        {
            "venta_id": venta_id,
            "cliente_id": venta.ClienteID,
            "vendedor_id": venta.VendedorID,
            "territorio_id": venta.TerritorioID,
            "observaciones": venta.Observaciones,
        },
    )


def agregar_detalle(venta_id: int, detalle: VentaDetalleCreateRequest) -> None:
    """Agrega un detalle a una venta."""
    _ejecutar_comando(
        "dbo.USP_VentaDetalleAgregar",
        {
            "venta_id": venta_id,
            "producto_id": detalle.ProductoID,
            "cantidad": detalle.Cantidad,
            "precio_unitario": detalle.PrecioUnitario,
        },
    )


def actualizar_detalle(venta_id: int, detalle_id: int, detalle: VentaDetalleUpdateRequest) -> None:
    """Actualiza un detalle existente."""
    _ejecutar_comando(
        "dbo.USP_VentaDetalleActualizar",
        {
            "venta_id": venta_id,
            "venta_detalle_id": detalle_id,
            "producto_id": detalle.ProductoID,
            "cantidad": detalle.Cantidad,
            "precio_unitario": detalle.PrecioUnitario,
        },
    )


def eliminar_detalle(venta_id: int, detalle_id: int) -> None:
    """Desactiva un detalle de venta."""
    _ejecutar_comando(
        "dbo.USP_VentaDetalleEliminar",
        {
            "venta_id": venta_id,
            "venta_detalle_id": detalle_id,
        },
    )


def anular_venta(venta_id: int, motivo: str | None) -> None:
    """Anula una venta."""
    _ejecutar_comando(
        "dbo.USP_VentaAnular",
        {
            "venta_id": venta_id,
            "motivo": motivo,
        },
    )

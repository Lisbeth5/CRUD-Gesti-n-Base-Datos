from repositories import ventas_repository
from schemas.ventas import (
    MensajeResponse,
    VentaCreateRequest,
    VentaDetalleCreateRequest,
    VentaDetalleResponse,
    VentaDetalleUpdateRequest,
    VentaResponse,
)
from utils.exceptions import AppError


def listar_ventas(venta_id: int | None, cliente_id: int | None, vendedor_id: int | None, fecha_desde: str | None, fecha_hasta: str | None) -> list[VentaResponse]:
    """Consulta ventas registradas."""
    filas = ventas_repository.listar_ventas(venta_id, cliente_id, vendedor_id, fecha_desde, fecha_hasta)
    return [VentaResponse.model_validate({**fila, "Detalles": []}) for fila in filas]


def obtener_venta(venta_id: int) -> VentaResponse:
    """Obtiene una venta completa con sus detalles."""
    data = ventas_repository.obtener_venta(venta_id)
    if not data or not data["cabecera"]:
        raise AppError("Venta no encontrada")

    cabecera = data["cabecera"]
    detalles = [VentaDetalleResponse.model_validate(detalle) for detalle in data["detalles"]]
    return VentaResponse.model_validate({**cabecera, "Detalles": detalles})


def crear_venta(venta: VentaCreateRequest) -> VentaResponse:
    """Registra una nueva venta."""
    venta_id = ventas_repository.crear_venta(venta)
    return obtener_venta(venta_id)


def actualizar_venta(venta_id: int, venta: VentaCreateRequest) -> MensajeResponse:
    """Actualiza la cabecera de una venta."""
    ventas_repository.actualizar_venta(venta_id, venta)
    return MensajeResponse(mensaje=f"Venta {venta_id} actualizada exitosamente")


def agregar_detalle(venta_id: int, detalle: VentaDetalleCreateRequest) -> MensajeResponse:
    """Agrega un detalle a una venta."""
    ventas_repository.agregar_detalle(venta_id, detalle)
    return MensajeResponse(mensaje="Detalle agregado exitosamente")


def actualizar_detalle(venta_id: int, detalle_id: int, detalle: VentaDetalleUpdateRequest) -> MensajeResponse:
    """Actualiza un detalle existente de una venta."""
    ventas_repository.actualizar_detalle(venta_id, detalle_id, detalle)
    return MensajeResponse(mensaje="Detalle actualizado exitosamente")


def eliminar_detalle(venta_id: int, detalle_id: int) -> MensajeResponse:
    """Desactiva un detalle de una venta."""
    ventas_repository.eliminar_detalle(venta_id, detalle_id)
    return MensajeResponse(mensaje="Detalle eliminado exitosamente")


def anular_venta(venta_id: int, motivo: str | None) -> MensajeResponse:
    """Anula una venta."""
    ventas_repository.anular_venta(venta_id, motivo)
    return MensajeResponse(mensaje=f"Venta {venta_id} anulada exitosamente")

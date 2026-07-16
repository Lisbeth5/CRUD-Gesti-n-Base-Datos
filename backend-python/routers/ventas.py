from fastapi import APIRouter, Query

from schemas.ventas import (
    MensajeResponse,
    VentaCreateRequest,
    VentaDetalleCreateRequest,
    VentaDetalleUpdateRequest,
    VentaResponse,
)
from services import ventas_service

router = APIRouter(prefix="/api/ventas", tags=["Ventas"])


@router.get("", response_model=list[VentaResponse])
def listar_ventas(
    venta_id: int | None = Query(default=None, ge=1),
    cliente_id: int | None = Query(default=None, ge=1),
    vendedor_id: int | None = Query(default=None, ge=1),
    fecha_desde: str | None = Query(default=None),
    fecha_hasta: str | None = Query(default=None),
) -> list[VentaResponse]:
    """Lista ventas registradas."""
    return ventas_service.listar_ventas(venta_id, cliente_id, vendedor_id, fecha_desde, fecha_hasta)


@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_venta(venta_id: int) -> VentaResponse:
    """Obtiene una venta completa con sus detalles."""
    return ventas_service.obtener_venta(venta_id)


@router.post("", response_model=VentaResponse)
def crear_venta(venta: VentaCreateRequest) -> VentaResponse:
    """Registra una nueva venta."""
    return ventas_service.crear_venta(venta)


@router.put("/{venta_id}", response_model=MensajeResponse)
def actualizar_venta(venta_id: int, venta: VentaCreateRequest) -> MensajeResponse:
    """Actualiza una venta existente."""
    return ventas_service.actualizar_venta(venta_id, venta)


@router.post("/{venta_id}/detalle", response_model=MensajeResponse)
def agregar_detalle(venta_id: int, detalle: VentaDetalleCreateRequest) -> MensajeResponse:
    """Agrega un detalle a una venta."""
    return ventas_service.agregar_detalle(venta_id, detalle)


@router.put("/{venta_id}/detalle/{detalle_id}", response_model=MensajeResponse)
def actualizar_detalle(venta_id: int, detalle_id: int, detalle: VentaDetalleUpdateRequest) -> MensajeResponse:
    """Actualiza un detalle existente de una venta."""
    return ventas_service.actualizar_detalle(venta_id, detalle_id, detalle)


@router.delete("/{venta_id}/detalle/{detalle_id}", response_model=MensajeResponse)
def eliminar_detalle(venta_id: int, detalle_id: int) -> MensajeResponse:
    """Elimina un detalle de una venta."""
    return ventas_service.eliminar_detalle(venta_id, detalle_id)


@router.post("/{venta_id}/anular", response_model=MensajeResponse)
def anular_venta(venta_id: int, motivo: str | None = None) -> MensajeResponse:
    """Anula una venta."""
    return ventas_service.anular_venta(venta_id, motivo)

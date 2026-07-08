from fastapi import APIRouter

from schemas.clientes import ClienteCreate, ClienteResponse, ClienteUpdate, MensajeResponse
from services import clientes_service


router = APIRouter(prefix="/api/clientes", tags=["Clientes"])


@router.get("", response_model=list[ClienteResponse])
def listar_clientes() -> list[ClienteResponse]:
    """Lista clientes delegando la operacion al servicio."""
    return clientes_service.listar_clientes()


@router.post("", response_model=MensajeResponse)
def crear_cliente(cliente: ClienteCreate) -> MensajeResponse:
    """Crea un cliente sin contener logica SQL en el endpoint."""
    return clientes_service.crear_cliente(cliente)


@router.put("/{customer_id}", response_model=MensajeResponse)
def actualizar_cliente(customer_id: int, cliente: ClienteUpdate) -> MensajeResponse:
    """Actualiza un cliente existente por identificador."""
    return clientes_service.actualizar_cliente(customer_id, cliente)


@router.delete("/{customer_id}", response_model=MensajeResponse)
def eliminar_cliente(customer_id: int) -> MensajeResponse:
    """Elimina un cliente mediante el servicio correspondiente."""
    return clientes_service.eliminar_cliente(customer_id)

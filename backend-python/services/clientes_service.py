from repositories import clientes_repository
from schemas.clientes import ClienteCreate, ClienteResponse, ClienteUpdate, MensajeResponse


def listar_clientes() -> list[ClienteResponse]:
    """Obtiene clientes y los valida contra el contrato de salida."""
    clientes = clientes_repository.listar_clientes()
    return [ClienteResponse.model_validate(cliente) for cliente in clientes]


def crear_cliente(cliente: ClienteCreate) -> MensajeResponse:
    """Coordina el registro de un cliente."""
    clientes_repository.crear_cliente(cliente)
    return MensajeResponse(mensaje="Cliente creado exitosamente")


def actualizar_cliente(customer_id: int, cliente: ClienteUpdate) -> MensajeResponse:
    """Coordina la actualizacion de un cliente existente."""
    clientes_repository.actualizar_cliente(customer_id, cliente)
    return MensajeResponse(mensaje=f"Cliente {customer_id} modificado exitosamente")


def eliminar_cliente(customer_id: int) -> MensajeResponse:
    """Coordina la eliminacion de un cliente."""
    clientes_repository.eliminar_cliente(customer_id)
    return MensajeResponse(mensaje=f"Cliente {customer_id} eliminado de la base de datos")

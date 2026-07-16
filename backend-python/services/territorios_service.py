from repositories import territorios_repository
from schemas.territorios import MensajeResponse, TerritorioCreate, TerritorioResponse, TerritorioUpdate
from utils.exceptions import AppError


def listar_territorios(territorio_id: int | None) -> list[TerritorioResponse]:
    """Obtiene territorios y valida la respuesta pública."""
    filas = territorios_repository.listar_territorios(territorio_id)
    return [TerritorioResponse.model_validate(fila) for fila in filas]


def crear_territorio(territorio: TerritorioCreate) -> MensajeResponse:
    """Registra un territorio."""
    territorios_repository.crear_territorio(territorio)
    return MensajeResponse(mensaje="Territorio creado exitosamente")


def actualizar_territorio(territorio_id: int, territorio: TerritorioUpdate) -> MensajeResponse:
    """Actualiza un territorio existente."""
    territorios_repository.actualizar_territorio(territorio_id, territorio)
    return MensajeResponse(mensaje=f"Territorio {territorio_id} actualizado exitosamente")


def eliminar_territorio(territorio_id: int) -> MensajeResponse:
    """Elimina un territorio."""
    territorios_repository.eliminar_territorio(territorio_id)
    return MensajeResponse(mensaje=f"Territorio {territorio_id} eliminado exitosamente")

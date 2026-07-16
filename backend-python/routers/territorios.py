from fastapi import APIRouter, Query

from schemas.territorios import MensajeResponse, TerritorioCreate, TerritorioResponse, TerritorioUpdate
from services import territorios_service

router = APIRouter(prefix="/api/territorios", tags=["Territorios"])


@router.get("", response_model=list[TerritorioResponse])
def listar_territorios(territorio_id: int | None = Query(default=None, ge=1)) -> list[TerritorioResponse]:
    """Lista territorios de la base de datos."""
    return territorios_service.listar_territorios(territorio_id)


@router.post("", response_model=MensajeResponse)
def crear_territorio(territorio: TerritorioCreate) -> MensajeResponse:
    """Crea un territorio."""
    return territorios_service.crear_territorio(territorio)


@router.put("/{territorio_id}", response_model=MensajeResponse)
def actualizar_territorio(territorio_id: int, territorio: TerritorioUpdate) -> MensajeResponse:
    """Actualiza los datos de un territorio."""
    return territorios_service.actualizar_territorio(territorio_id, territorio)


@router.delete("/{territorio_id}", response_model=MensajeResponse)
def eliminar_territorio(territorio_id: int) -> MensajeResponse:
    """Elimina un territorio."""
    return territorios_service.eliminar_territorio(territorio_id)

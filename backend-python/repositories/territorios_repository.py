from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.database import get_engine
from schemas.territorios import TerritorioCreate, TerritorioUpdate
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


def listar_territorios(territorio_id: int | None) -> list[dict]:
    """Consulta territorios de Sales.SalesTerritory."""
    return _ejecutar_listado(
        "dbo.USP_TerritorioListar",
        {"territorio_id": territorio_id},
    )


def crear_territorio(territorio: TerritorioCreate) -> None:
    """Crea un territorio mediante procedimiento almacenado."""
    _ejecutar_comando(
        "dbo.USP_TerritorioCrear",
        {
            "name": territorio.Name,
            "country_region_code": territorio.CountryRegionCode,
            "group": territorio.Group,
            "sales_ytd": territorio.SalesYTD,
            "sales_last_year": territorio.SalesLastYear,
            "cost_ytd": territorio.CostYTD,
            "cost_last_year": territorio.CostLastYear,
        },
    )


def actualizar_territorio(territorio_id: int, territorio: TerritorioUpdate) -> None:
    """Actualiza los datos de un territorio."""
    _ejecutar_comando(
        "dbo.USP_TerritorioActualizar",
        {
            "territorio_id": territorio_id,
            "name": territorio.Name,
            "country_region_code": territorio.CountryRegionCode,
            "group": territorio.Group,
            "sales_ytd": territorio.SalesYTD,
            "sales_last_year": territorio.SalesLastYear,
            "cost_ytd": territorio.CostYTD,
            "cost_last_year": territorio.CostLastYear,
        },
    )


def eliminar_territorio(territorio_id: int) -> None:
    """Elimina un territorio."""
    _ejecutar_comando(
        "dbo.USP_TerritorioEliminar",
        {"territorio_id": territorio_id},
    )

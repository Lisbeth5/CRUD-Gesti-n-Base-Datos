from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.database import get_engine
from schemas.clientes import ClienteCreate, ClienteUpdate
from utils.exceptions import DatabaseError


def listar_clientes() -> list[dict]:
    """Ejecuta el procedimiento almacenado que lista clientes."""
    try:
        with get_engine().connect() as connection:
            result = connection.execute(text("EXEC Sales.USP_ListarClientes"))
            return [
                {
                    "CustomerID": row.CustomerID,
                    "PersonID": row.PersonID,
                    "FirstName": row.FirstName,
                    "LastName": row.LastName,
                    "TerritoryID": row.TerritoryID,
                    "AccountNumber": row.AccountNumber,
                }
                for row in result
            ]
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al listar clientes: {exc}") from exc


def crear_cliente(cliente: ClienteCreate) -> None:
    """Ejecuta el procedimiento almacenado que inserta un cliente."""
    try:
        with get_engine().begin() as connection:
            connection.execute(
                text("EXEC Sales.USP_InsertarCliente :fname, :lname, :territorio"),
                {
                    "fname": cliente.FirstName,
                    "lname": cliente.LastName,
                    "territorio": cliente.TerritoryID,
                },
            )
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al crear cliente: {exc}") from exc


def actualizar_cliente(customer_id: int, cliente: ClienteUpdate) -> None:
    """Ejecuta el procedimiento almacenado que actualiza un cliente."""
    try:
        with get_engine().begin() as connection:
            connection.execute(
                text("EXEC Sales.USP_ActualizarCliente :id, :fname, :lname, :territorio"),
                {
                    "id": customer_id,
                    "fname": cliente.FirstName,
                    "lname": cliente.LastName,
                    "territorio": cliente.TerritoryID,
                },
            )
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al actualizar cliente {customer_id}: {exc}") from exc


def eliminar_cliente(customer_id: int) -> None:
    """Ejecuta el procedimiento almacenado que elimina un cliente."""
    try:
        with get_engine().begin() as connection:
            connection.execute(
                text("EXEC Sales.USP_EliminarCliente :id"),
                {"id": customer_id},
            )
    except SQLAlchemyError as exc:
        raise DatabaseError(f"Error al eliminar cliente {customer_id}: {exc}") from exc

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


# Cadena de conexion centralizada para AdventureWorks2025 en SQL Server.
CONNECTION_STRING = (
    "mssql+pyodbc://localhost/AdventureWorks2025"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)


# El engine se reutiliza en toda la aplicacion mediante los repositorios.
engine = create_engine(CONNECTION_STRING, pool_pre_ping=True)


def get_engine() -> Engine:
    """Retorna el engine compartido de SQLAlchemy."""
    return engine

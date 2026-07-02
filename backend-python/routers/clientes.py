""" 
from fastapi import APIRouter

# Definimos el enrutador que main.py va a buscar
router = APIRouter()

@router.get("/api/clientes")
def obtener_clientes():
    return {"mensaje": "¡Conexión exitosa a la API de Clientes!"}
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict  # 🛠️ Se agrega ConfigDict aquí
from sqlalchemy import text
from main import engine

router = APIRouter()

# --- MODELO DE DATOS RECIBIDO DESDE BLAZOR ---
class ClienteDTO(BaseModel):
    FirstName: str
    LastName: str
    TerritoryID: int

    # 🛠️ ESTA CONFIGURACIÓN SOLUCIONA EL ERROR:
    # Mapea dinámicamente campos que vengan en minúsculas (como 'firstName') a las propiedades en mayúsculas.
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda field_name: field_name[0].lower() + field_name[1:] if field_name else field_name
    )

# 1. OBTENER TODOS LOS CLIENTES (READ)
@router.get("/api/clientes")
def listar_clientes():
    try:
        with engine.connect() as con:
            result = con.execute(text("EXEC Sales.USP_ListarClientes"))
            # Transformamos los objetos fila en diccionarios serializables
            clientes = [
                {
                    "CustomerID": row.CustomerID,
                    "PersonID": row.PersonID,
                    "FirstName": row.FirstName,
                    "LastName": row.LastName,
                    "TerritoryID": row.TerritoryID,
                    "AccountNumber": row.AccountNumber
                }
                for row in result
            ]
            return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

# 2. CREAR UN CLIENTE (CREATE)
@router.post("/api/clientes")
def crear_cliente(cliente: ClienteDTO):
    try:
        with engine.begin() as con:  # engine.begin maneja automáticamente transacciones
            con.execute(
                text("EXEC Sales.USP_InsertarCliente :fname, :lname, :territorio"),
                {
                    "fname": cliente.FirstName,
                    "lname": cliente.LastName,
                    "territorio": cliente.TerritoryID
                }
            )
            return {"mensaje": "Cliente creado exitosamente desde Procedimiento Almacenado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. ACTUALIZAR UN CLIENTE (UPDATE)
@router.put("/api/clientes/{customer_id}")
def actualizar_cliente(customer_id: int, cliente: ClienteDTO):
    try:
        with engine.begin() as con:
            con.execute(
                text("EXEC Sales.USP_ActualizarCliente :id, :fname, :lname, :territorio"),
                {
                    "id": customer_id,
                    "fname": cliente.FirstName,
                    "lname": cliente.LastName,
                    "territorio": cliente.TerritoryID
                }
            )
            return {"mensaje": f"Cliente {customer_id} modificado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. ELIMINAR UN CLIENTE (DELETE)
@router.delete("/api/clientes/{customer_id}")
def eliminar_cliente(customer_id: int):
    try:
        with engine.begin() as con:
            con.execute(text("EXEC Sales.USP_EliminarCliente :id"), {"id": customer_id})
            return {"mensaje": f"Cliente {customer_id} eliminado de la base de datos"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine

# 1. Instanciamos la aplicación de FastAPI
app = FastAPI(title="Backend AdventureWorks Sales")

# 2. Permitir que Blazor se comunique con Python sin bloqueos de seguridad (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Configuración global de la conexión a SQL Server
CONN_STR = "mssql+pyodbc://localhost/AdventureWorks2025?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(CONN_STR)

# 4. Endpoint base para verificar que el backend responda
@app.get("/")
def inicio():
    return {"mensaje": "Servidor Python conectado y corriendo"}

# 5. IMPORTACIÓN Y REGISTRO DE LOS ENRUTADORES (ROUTERS)
# Nota: Importamos el router AQUÍ abajo para evitar problemas de importación circular
from routers import clientes

app.include_router(clientes.router)

# Nota: A medida que crees los otros módulos del ingeniero, solo los agregas aquí:
# from routers import vendedores
# app.include_router(vendedores.router)
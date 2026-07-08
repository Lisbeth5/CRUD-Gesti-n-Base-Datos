from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class DetalleVentaResponse(BaseModel):
    """Fila del reporte detallado de ventas."""

    Fecha: date
    NumeroOrden: str
    Cliente: str
    Vendedor: str
    Producto: str
    Cantidad: int
    PrecioUnitario: Decimal
    TotalLinea: Decimal


class ResumenVentaResponse(BaseModel):
    """Fila del reporte resumido de ventas por cliente y vendedor."""

    Cliente: str
    Vendedor: str
    NumeroPedidos: int
    TotalVendido: Decimal


class VentaProductoResponse(BaseModel):
    """Fila del reporte de ventas agrupadas por producto."""

    Producto: str
    CantidadVendida: int
    TotalVendido: Decimal


class VentaCategoriaResponse(BaseModel):
    """Fila del reporte de ventas agrupadas por categoria."""

    Categoria: str
    CantidadVendida: int
    TotalVendido: Decimal


class VentaTerritorioResponse(BaseModel):
    """Fila del reporte de ventas por territorio, categoria y producto."""

    Territorio: str
    Categoria: str
    Producto: str
    Cantidad: int
    TotalVendido: Decimal

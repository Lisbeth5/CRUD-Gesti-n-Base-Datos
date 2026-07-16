from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


def to_camel_case(field_name: str) -> str:
    """Convierte nombres PascalCase a camelCase para aceptar JSON del frontend."""
    return field_name[0].lower() + field_name[1:] if field_name else field_name


class VentaBaseModel(BaseModel):
    """Modelo base con alias camelCase para ventas."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel_case)


class VentaCreateRequest(VentaBaseModel):
    """Datos requeridos para registrar una venta."""

    ClienteID: int = Field(..., ge=1)
    VendedorID: int | None = None
    TerritorioID: int | None = None
    Observaciones: str | None = None


class VentaDetalleCreateRequest(VentaBaseModel):
    """Datos requeridos para agregar un producto a una venta."""

    ProductoID: int = Field(..., ge=1)
    Cantidad: int = Field(..., ge=1)
    PrecioUnitario: float = Field(..., ge=0)


class VentaDetalleUpdateRequest(VentaBaseModel):
    """Datos editables de un detalle de venta."""

    ProductoID: int = Field(..., ge=1)
    Cantidad: int = Field(..., ge=1)
    PrecioUnitario: float = Field(..., ge=0)


class VentaDetalleResponse(VentaBaseModel):
    """Detalle de venta retornado al frontend."""

    VentaDetalleID: int
    VentaID: int
    ProductoID: int
    Cantidad: int
    PrecioUnitario: float
    Importe: float
    Activo: bool


class VentaResponse(VentaBaseModel):
    """Cabecera de venta retornada al frontend."""

    VentaID: int
    ClienteID: int
    VendedorID: int | None = None
    TerritorioID: int | None = None
    FechaVenta: datetime
    Estado: str
    Anulada: bool
    FechaAnulacion: datetime | None = None
    TotalVenta: float
    Observaciones: str | None = None
    ItemCount: int = 0
    Detalles: list[VentaDetalleResponse] = Field(default_factory=list)


class MensajeResponse(VentaBaseModel):
    """Respuesta simple para operaciones de ventas."""

    mensaje: str

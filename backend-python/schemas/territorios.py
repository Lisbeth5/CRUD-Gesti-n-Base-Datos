from pydantic import BaseModel, ConfigDict, Field


def to_camel_case(field_name: str) -> str:
    """Convierte nombres PascalCase a camelCase para aceptar JSON del frontend."""
    return field_name[0].lower() + field_name[1:] if field_name else field_name


class TerritorioBaseModel(BaseModel):
    """Modelo base con alias camelCase para territorios."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel_case)


class TerritorioCreate(TerritorioBaseModel):
    """Datos requeridos para crear un territorio."""

    Name: str = Field(..., min_length=3, max_length=50)
    CountryRegionCode: str = Field(..., min_length=2, max_length=3)
    Group: str = Field(..., min_length=3, max_length=50)
    SalesYTD: float = Field(default=0.0)
    SalesLastYear: float = Field(default=0.0)
    CostYTD: float = Field(default=0.0)
    CostLastYear: float = Field(default=0.0)


class TerritorioUpdate(TerritorioBaseModel):
    """Datos editables de un territorio."""

    Name: str = Field(..., min_length=3, max_length=50)
    CountryRegionCode: str = Field(..., min_length=2, max_length=3)
    Group: str = Field(..., min_length=3, max_length=50)
    SalesYTD: float = Field(default=0.0)
    SalesLastYear: float = Field(default=0.0)
    CostYTD: float = Field(default=0.0)
    CostLastYear: float = Field(default=0.0)


class TerritorioResponse(TerritorioBaseModel):
    """Datos públicos de un territorio."""

    TerritoryID: int
    Name: str
    CountryRegionCode: str
    Group: str
    SalesYTD: float
    SalesLastYear: float
    CostYTD: float
    CostLastYear: float


class MensajeResponse(TerritorioBaseModel):
    """Respuesta simple para operaciones administrativas."""

    mensaje: str

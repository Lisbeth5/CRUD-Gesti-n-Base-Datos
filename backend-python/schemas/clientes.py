from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ClienteBase(BaseModel):
    """Campos recibidos desde Blazor para crear o actualizar clientes."""

    FirstName: str = Field(
        ...,
        min_length=1,
        max_length=50,
        validation_alias=AliasChoices("FirstName", "firstName"),
    )
    LastName: str = Field(
        ...,
        min_length=1,
        max_length=50,
        validation_alias=AliasChoices("LastName", "lastName"),
    )
    TerritoryID: int = Field(
        ...,
        ge=1,
        le=10,
        validation_alias=AliasChoices("TerritoryID", "territoryID", "territoryId"),
    )

    model_config = ConfigDict(populate_by_name=True)


class ClienteCreate(ClienteBase):
    """Contrato de entrada para registrar clientes."""


class ClienteUpdate(ClienteBase):
    """Contrato de entrada para actualizar clientes."""


class ClienteResponse(BaseModel):
    """Contrato de salida para mostrar clientes en Blazor."""

    CustomerID: int
    PersonID: int | None = None
    FirstName: str | None = None
    LastName: str | None = None
    TerritoryID: int
    AccountNumber: str | None = None


class MensajeResponse(BaseModel):
    """Respuesta simple para operaciones de escritura."""

    mensaje: str

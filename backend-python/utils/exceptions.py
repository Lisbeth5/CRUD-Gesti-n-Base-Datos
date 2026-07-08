class AppError(Exception):
    """Error controlado que puede transformarse en una respuesta HTTP."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class DatabaseError(AppError):
    """Error producido durante el acceso a SQL Server."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=500)

class BoundaryError(Exception):
    def __init__(self, exit_code: int, message: str) -> None:
        self.exit_code = exit_code
        self.message = message
        super().__init__(message)


E001_MESSAGE = "Invalid format. Use unit:value (ex: meter:2.5)"
E002_TEMPLATE = "Invalid number: {token}"
E003_TEMPLATE = "Unknown unit: {unit}"
E004_TEMPLATE = "Negative value not allowed: {value}"

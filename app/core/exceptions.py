class CustomException(Exception):
    """Base class for all custom exceptions in the application."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

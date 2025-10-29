from typing import Optional
from fastapi import HTTPException


class BaseException(HTTPException):
    def __init__(
        self,
        message: Optional[str] = None,
        error: Optional[str] = None,
        status_code: Optional[int] = None,
        action: Optional[str] = None,
    ) -> None:
        self.message = message or "Internal error occured in the API"
        self.error = error or "InternalServerError"
        self.action = action or "Contact the support for more information"
        self.status_code = status_code or 500
        super().__init__(
            status_code=self.status_code,
            detail={
                "error": self.error,
                "message": self.message,
                "action": self.action,
            },
        )


class ConflictException(BaseException):
    def __init__(self, resource_name: str, identifier: str) -> None:
        message = (
            f"A '{resource_name}' with the identifier '{identifier}' already exists"
        )
        error = "ConflictError"
        status_code = 409
        action = "The resource could not be created. Please try again with a different identifier"
        super().__init__(message, error, status_code, action)


class UnauthenticatedExpection(BaseException):
    def __init__(self, custom_message: Optional[str | None] = None):
        message = custom_message or "Invalid or expired authorization token"
        error = "UnauthorizedError"
        status_code = 401
        action = "Provide a valid authorization token"
        super().__init__(message, error, status_code, action)


class BadRequestException(BaseException):
    def __init__(self, custom_message: Optional[str | None] = None):
        message = custom_message or "The request sended was malformed"
        error = "BadRequestError"
        status_code = 400
        action = "Send a valid request to the server"
        super().__init__(message, error, status_code, action)

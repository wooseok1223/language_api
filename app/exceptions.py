class Exception(Exception):
    error_code = "SERVER_ERROR"
    status_code = 500

    def __init__(self, error_message: str = None):
        self.error_message = error_message

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        if self.error_message:
            return f"{class_name}(status_code={self.status_code}, error_code: {self.error_code}, error_message: {self.error_message})"
        return f"{class_name}(status_code={self.status_code}, error_code: {self.error_code})"

    def __str__(self) -> str:
        return self.__repr__()


class KeyException(Exception):
    error_code = "KEY_ERROR"


class HTTPException(Exception):
    def __init__(self, status_code: int, error_code: str, error_message: str = None, card_error_message: str = None):
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
        self.card_error_message = card_error_message

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code}, error_code: {self.error_code}, error_message: {self.error_message})"


class ClientException(HTTPException):
    """
    클라이언트측 에러
    """

    def __init__(
            self,
            *,
            status_code: int = 400,
            error_code: str = "BAD_REQUEST",
            error_message: str = None
    ):
        super().__init__(
            status_code=status_code,
            error_code=error_code,
            error_message=error_message
        )


class ServerException(HTTPException):
    """
    서버측 에러
    """

    def __init__(self, *, status_code: int = 500, error_code: str = "INTERNAL_SERVER_ERROR", error_message: str = None):
        super().__init__(status_code=status_code, error_code=error_code, error_message=error_message)


class NotFoundException(ClientException):
    """해당 자원이 존재하지 않음"""

    def __init__(self, error_message: str = None):
        super().__init__(status_code=404, error_code="NOT_FOUND_ERROR", error_message=error_message)


class SQLException(ServerException):
    """SQL 실행 시 에러"""

    def __init__(self, *, error_message: str = None):
        super().__init__(status_code=500, error_code="SQL_EXCEPTION", error_message=error_message)

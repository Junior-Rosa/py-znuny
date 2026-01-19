

from typing import Any, Mapping

class TicketClientError(Exception):
    """
    Docstring for TicketClientError
    Represents an error returned by the TicketClient API.
    """
    def __init__(self, error: Mapping[str, Any]) -> None:
        self.error = error
        code = error.get("ErrorCode")
        message = error.get("ErrorMessage") or "Unknown error"
        super().__init__(f"{code}: {message}" if code else str(message))
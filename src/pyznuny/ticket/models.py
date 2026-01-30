from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Mapping

from pydantic import BaseModel

HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]

def _clean_dict(data: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


def _require_non_empty(value: str, field: str) -> None:
    if not value or not str(value).strip():
        raise ValueError(f"{field} is required.")

def _normalize_path(path: str) -> str:
    normalized = "/" + path.lstrip("/")
    if normalized == "/":
        raise ValueError("Endpoint path cannot be empty.")
    return normalized


def _join_base_path(base_path: str, endpoint_path: str) -> str:
    base = base_path.strip("/")
    tail = endpoint_path.lstrip("/")
    if not base:
        return "/" + tail
    return f"/{base}/{tail}"

class Endpoint(BaseModel):
    """
    Object representing an API endpoint

    :arg name: Name of the endpoint
    :type name: str
    :arg method: HTTP method for the endpoint
    :type method: HttpMethod
    :arg path: Endpoint path
    :type path: str
    :raises pydantic.ValidationError: If http method is invalid
    :raises ValueError: If endpoint path is empty
    """
    name: str
    method: HttpMethod
    path: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", _normalize_path(self.path))

    def full_path(self, base_path: str = "") -> str:
        """
        Returns the full path for the endpoint

        :param base_path: Base path for the endpoint, defaults to an empty string
        :type base_path: str
        :return: Full path for the endpoint
        :rtype: str
        """
        return _join_base_path(base_path, self.path)



@dataclass(slots=True)
class TicketCreateTicket:
    """
    Represents the metadata for a ticket

    :param Title: Title of the ticket
    :type Title: str
    :param Queue: Queue of the ticket
    :type Queue: str
    :param State: State of the ticket
    :type State: str
    :param Priority: Priority of the ticket
    :type Priority: str
    :param CustomerUser: Customer user of the ticket
    :type CustomerUser: str | None
    :param Type: Type of the ticket
    :type Type: str | None
    :param Service: Service of the ticket
    :type Service: str | None
    :param SLA: SLA of the ticket
    :type SLA: str | None
    :param Owner: Owner of the ticket
    :type Owner: str | None
    :raises ValueError: If any required field is empty
    """
    Title: str
    Queue: str
    State: str
    Priority: str
    CustomerUser: str | None = None
    Type: str | None = None
    Service: str | None = None
    SLA: str | None = None
    Owner: str | None = None
    Responsible: str | None = None

    def validate(self) -> None:
        _require_non_empty(self.Title, "Ticket.Title")
        _require_non_empty(self.Queue, "Ticket.Queue")
        _require_non_empty(self.State, "Ticket.State")
        _require_non_empty(self.Priority, "Ticket.Priority")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return _clean_dict(
            {
                "Title": self.Title,
                "Queue": self.Queue,
                "State": self.State,
                "Priority": self.Priority,
                "CustomerUser": self.CustomerUser,
                "Type": self.Type,
                "Service": self.Service,
                "SLA": self.SLA,
                "Owner": self.Owner,
                "Responsible": self.Responsible,
            }
        )


@dataclass(slots=True)
class TicketCreateArticle:
    """
    Represents the article content for a ticket

    :param Subject: Subject of the article
    :type Subject: str
    :param Body: Body of the article
    :type Body: str
    :param ContentType: Content type of the article
    :type ContentType: str
    :param Charset: Charset of the article, defaults to None
    :type Charset: str | None
    :param MimeType: MIME type of the article, defaults to None
    :type MimeType: str | None
    :param SenderType: Sender type of the article, defaults to None
    :type SenderType: str | None
    :param From_: From address of the article, defaults to None
    :type From_: str | None
    :raises ValueError: If any required field is empty
    """
    Subject: str
    Body: str
    ContentType: str
    Charset: str | None = None
    MimeType: str | None = None
    SenderType: str | None = None
    From_: str | None = None

    def validate(self) -> None:
        _require_non_empty(self.Subject, "Article.Subject")
        _require_non_empty(self.Body, "Article.Body")
        _require_non_empty(self.ContentType, "Article.ContentType")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return _clean_dict(
            {
                "Subject": self.Subject,
                "Body": self.Body,
                "ContentType": self.ContentType,
                "Charset": self.Charset,
                "MimeType": self.MimeType,
                "SenderType": self.SenderType,
                "From": self.From_,
            }
        )


@dataclass(slots=True)
class TicketCreatePayload:
    """
    Represents the payload for creating a ticket

    :param Ticket: Ticket metadata
    :type Ticket: TicketCreateTicket
    :param Article: Article content
    :type Article: TicketCreateArticle
    :param DynamicField: Dynamic fields for the ticket, defaults to None
    :type DynamicField: Mapping[str, Any] | None
    :param Attachment: Attachments for the ticket, defaults to None
    :type Attachment: list[Mapping[str, Any]] | None
    :param TimeUnit: Time unit for the ticket, defaults to None
    :type TimeUnit: int | None
    """
    Ticket: TicketCreateTicket
    Article: TicketCreateArticle
    DynamicField: Mapping[str, Any] | None = None
    Attachment: list[Mapping[str, Any]] | None = None
    TimeUnit: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return _clean_dict(
            {
                "Ticket": self.Ticket.to_dict(),
                "Article": self.Article.to_dict(),
                "DynamicField": self.DynamicField,
                "Attachment": self.Attachment,
                "TimeUnit": self.TimeUnit,
            }
        )



class TicketUpdateTicket(TicketCreateTicket):
    def validate(self):
        pass
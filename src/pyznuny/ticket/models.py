from __future__ import annotations

import base64
import binascii
from typing import Any, Literal, Mapping

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]

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

    model_config = ConfigDict(extra="ignore")

    @field_validator("path")
    @classmethod
    def _validate_path(cls, value: str) -> str:
        return _normalize_path(value)

    def full_path(self, base_path: str = "") -> str:
        """
        Returns the full path for the endpoint

        :param base_path: Base path for the endpoint, defaults to an empty string
        :type base_path: str
        :return: Full path for the endpoint
        :rtype: str
        """
        return _join_base_path(base_path, self.path)



class TicketCreateTicket(BaseModel):
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
    CustomerUser: str
    Priority: str | None = None
    PriorityID: int | None = None
    State: str | None = None
    StateID: int | None = None
    Type: str | None = None
    Service: str | None = None
    SLA: str | None = None
    Owner: str | None = None
    Responsible: str | None = None

    model_config = ConfigDict(extra="ignore")

    @field_validator("Title", "Queue", "CustomerUser")
    @classmethod
    def _validate_required(cls, value: str, info) -> str:
        _require_non_empty(value, f"Ticket.{info.field_name}")
        return value

    @model_validator(mode="after")
    def _validate_exactly_one_choices(self) -> "TicketCreateTicket":
        pairs = (
            ("State", self.State, self.StateID),
            ("Priority", self.Priority, self.PriorityID),
        )
        for name, text_value, id_value in pairs:
            has_text = bool(text_value is not None and str(text_value).strip())
            has_id = id_value is not None
            if has_text == has_id:
                raise ValueError(
                    f"Provide exactly one of Ticket.{name} or Ticket.{name}ID."
                )
            if has_text:
                _require_non_empty(text_value, f"Ticket.{name}")
        return self

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)


class TicketCreateArticle(BaseModel):
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
    ContentType: str | None = None
    Charset: str | None = None
    MimeType: str | None = None
    SenderType: str | None = None
    From_: str | None = Field(default=None, alias="From")
    Attachment: list["TicketCreateArticleAttachment"] | None = None

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    @field_validator("Subject", "Body")
    @classmethod
    def _validate_required(cls, value: str, info) -> str:
        _require_non_empty(value, f"Article.{info.field_name}")
        return value

    @field_validator("ContentType", "MimeType", "Charset")
    @classmethod
    def _validate_optional_non_empty(cls, value: str | None, info) -> str | None:
        if value is None:
            return value
        _require_non_empty(value, f"Article.{info.field_name}")
        return value

    @model_validator(mode="after")
    def _validate_content_type_choice(self) -> "TicketCreateArticle":
        has_content_type = (self.ContentType is not None and str(self.ContentType)
                            .strip())
        has_mime = self.MimeType is not None and str(self.MimeType).strip()
        has_charset = self.Charset is not None and str(self.Charset).strip()
        if not has_content_type and not (has_mime and has_charset):
            raise ValueError(
                "Provide Article.ContentType "
                "or both Article.MimeType and Article.Charset."
            )
        return self

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)

class TicketCreateArticleAttachment(BaseModel):
    """
    Represents an attachment for a ticket article

    :param Filename: Name of the attachment file
    :type Filename: str
    :param Content: Base64 encoded content of the attachment
    :type Content: str
    :param ContentType: MIME type of the attachment, defaults to None
    :type ContentType: str | None
    :raises ValueError: If any required field is empty
    """
    Filename: str
    Content: str
    ContentType: str | None = None

    model_config = ConfigDict(extra="ignore")

    @field_validator("Filename", "Content")
    @classmethod
    def _validate_required(cls, value: str, info) -> str:
        _require_non_empty(value, f"Attachment.{info.field_name}")
        return value

    @field_validator("Content")
    @classmethod
    def _validate_base64_content(cls, value: str) -> str:
        try:
            base64.b64decode(value, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("Attachment.Content must be valid base64.") from exc
        return value

    @field_validator("ContentType")
    @classmethod
    def _validate_optional_non_empty(cls, value: str | None, info) -> str | None:
        if value is None:
            return value
        _require_non_empty(value, f"Attachment.{info.field_name}")
        return value

class TicketCreatePayload(BaseModel):
    """
    Represents the payload for creating a ticket

    :param Ticket: Ticket metadata
    :type Ticket: TicketCreateTicket
    :param Article: Article content
    :type Article: TicketCreateArticle
    :param DynamicField: Dynamic fields for the ticket, defaults to None
    :type DynamicField: Mapping[str, Any] | None
    :param Attachment: Attachments for the ticket, defaults to None
    :type Attachment:
        list[TicketCreateArticleAttachment] | TicketCreateArticleAttachment | None
    :param TimeUnit: Time unit for the ticket, defaults to None
    :type TimeUnit: int | None
    """
    Ticket: TicketCreateTicket
    Article: TicketCreateArticle
    DynamicField: Mapping[str, Any] | None = None
    Attachment: (list[TicketCreateArticleAttachment] |
                 TicketCreateArticleAttachment |
                 None) = None
    TimeUnit: int | None = None

    model_config = ConfigDict(extra="ignore")

    @field_validator("Attachment", mode="before")
    @classmethod
    def _coerce_attachment_list(cls, value):
        if value is None:
            return value
        if isinstance(value, list):
            return value
        return [value]

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)


class TicketUpdateTicket(BaseModel):
    """
    Partial update payload for a ticket. All fields are optional, but if
    provided they must be non-empty strings.
    """
    Title: str | None = None
    Queue: str | None = None
    State: str | None = None
    Priority: str | None = None
    CustomerUser: str | None = None
    Type: str | None = None
    Service: str | None = None
    SLA: str | None = None
    Owner: str | None = None
    Responsible: str | None = None

    model_config = ConfigDict(extra="ignore")

    @field_validator(
        "Title",
        "Queue",
        "State",
        "Priority",
        "CustomerUser",
        "Type",
        "Service",
        "SLA",
        "Owner",
        "Responsible",
    )
    @classmethod
    def _validate_optional_non_empty(cls, value: str | None, info) -> str | None:
        if value is None:
            return value
        _require_non_empty(value, f"Ticket.{info.field_name}")
        return value

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)

import base64

import pytest
from pydantic import ValidationError

from src.pyznuny.ticket.models import (
    Endpoint,
    TicketCreateArticle,
    TicketCreateArticleAttachment,
    TicketCreatePayload,
    TicketCreateTicket,
    TicketUpdateTicket,
)


def _valid_ticket(overrides: dict | None = None) -> dict:
    data = {
        "Title": "Test Ticket",
        "Queue": "Raw",
        "CustomerUser": "user@example.com",
        "State": "open",
        "Priority": "3 normal",
    }
    if overrides:
        data.update(overrides)
    return data


def _valid_article(overrides: dict | None = None) -> dict:
    data = {
        "Subject": "Test Article",
        "Body": "This is a test article.",
        "ContentType": "text/plain; charset=utf8",
    }
    if overrides:
        data.update(overrides)
    return data


def test_ticket_create_ticket_requires_required_fields():
    with pytest.raises(ValidationError):
        TicketCreateTicket.model_validate(
            _valid_ticket({"Title": "   "})
        )

    with pytest.raises(ValidationError):
        TicketCreateTicket.model_validate(
            _valid_ticket({"Queue": ""})
        )

    with pytest.raises(ValidationError):
        TicketCreateTicket.model_validate(
            _valid_ticket({"CustomerUser": None})
        )


def test_ticket_create_ticket_state_exactly_one():
    with pytest.raises(ValidationError):
        TicketCreateTicket.model_validate(
            _valid_ticket({"State": "open", "StateID": 2})
        )

    with pytest.raises(ValidationError):
        TicketCreateTicket.model_validate(
            _valid_ticket({"State": None, "StateID": None})
        )

    TicketCreateTicket.model_validate(_valid_ticket({"State": "open"}))
    TicketCreateTicket.model_validate(_valid_ticket({"State": None, "StateID": 2}))


def test_ticket_create_ticket_priority_exactly_one():
    with pytest.raises(ValidationError):
        TicketCreateTicket.model_validate(
            _valid_ticket({"Priority": "3 normal", "PriorityID": 3})
        )

    with pytest.raises(ValidationError):
        TicketCreateTicket.model_validate(
            _valid_ticket({"Priority": None, "PriorityID": None})
        )

    TicketCreateTicket.model_validate(_valid_ticket({"Priority": "3 normal"}))
    TicketCreateTicket.model_validate(_valid_ticket({"Priority": None,
                                                     "PriorityID": 3}))


def test_article_requires_content_type_or_mime_and_charset():
    with pytest.raises(ValidationError):
        TicketCreateArticle.model_validate(
            _valid_article({"ContentType": None})
        )

    with pytest.raises(ValidationError):
        TicketCreateArticle.model_validate(
            _valid_article({"ContentType": None, "MimeType": "text/plain"})
        )

    TicketCreateArticle.model_validate(
        _valid_article({"ContentType": None,
                        "MimeType": "text/plain",
                        "Charset": "utf-8"})
    )

    TicketCreateArticle.model_validate(_valid_article({"ContentType": "text/plain"}))


def test_article_from_alias():
    article = TicketCreateArticle.model_validate(
        _valid_article({"From": "sender@example.com"})
    )
    assert article.From_ == "sender@example.com"
    assert article.model_dump(by_alias=True)["From"] == "sender@example.com"


def test_attachment_base64_validation():
    valid_b64 = base64.b64encode(b"content").decode()
    TicketCreateArticleAttachment.model_validate(
        {"Filename": "file.txt", "Content": valid_b64, "ContentType": "text/plain"}
    )

    with pytest.raises(ValidationError):
        TicketCreateArticleAttachment.model_validate(
            {"Filename": "file.txt",
             "Content": "not-base64",
             "ContentType": "text/plain"}
        )


def test_payload_attachment_single_is_coerced_to_list():
    valid_b64 = base64.b64encode(b"content").decode()
    payload = TicketCreatePayload.model_validate(
        {
            "Ticket": _valid_ticket(),
            "Article": _valid_article(),
            "Attachment": {
                "Filename": "file.txt",
                "Content": valid_b64,
                "ContentType": "text/plain",
            },
        }
    )
    assert isinstance(payload.Attachment, list)
    assert len(payload.Attachment) == 1


def test_endpoint_normalizes_path_and_full_path():
    endpoint = Endpoint(name="ticket_create", method="POST", path="tickets")
    assert endpoint.path == "/tickets"
    assert endpoint.full_path("/api") == "/api/tickets"

    endpoint = Endpoint(name="ticket_create", method="POST", path="/v1/tickets")
    assert endpoint.full_path("api") == "/api/v1/tickets"

    with pytest.raises(ValidationError):
        Endpoint(name="bad", method="POST", path="/")


def test_ticket_create_ticket_to_dict_excludes_none():
    ticket = TicketCreateTicket.model_validate(
        _valid_ticket({"State": None, "StateID": 1, "Priority": "3 normal"})
    )
    data = ticket.to_dict()
    assert data["StateID"] == 1
    assert "State" not in data


def test_article_to_dict_excludes_none():
    article = TicketCreateArticle.model_validate(
        _valid_article({"ContentType": "text/plain", "SenderType": None})
    )
    data = article.to_dict()
    assert "SenderType" not in data
    assert data["ContentType"] == "text/plain"


def test_attachment_optional_content_type_rejects_blank():
    valid_b64 = base64.b64encode(b"content").decode()
    with pytest.raises(ValidationError):
        TicketCreateArticleAttachment.model_validate(
            {"Filename": "file.txt", "Content": valid_b64, "ContentType": "   "}
        )


def test_payload_attachment_list_and_none_are_accepted():
    valid_b64 = base64.b64encode(b"content").decode()
    payload = TicketCreatePayload.model_validate(
        {
            "Ticket": _valid_ticket(),
            "Article": _valid_article(),
            "Attachment": [
                {
                    "Filename": "file.txt",
                    "Content": valid_b64,
                    "ContentType": "text/plain",
                }
            ],
        }
    )
    data = payload.to_dict()
    assert isinstance(data["Attachment"], list)
    assert len(data["Attachment"]) == 1

    payload_none = TicketCreatePayload.model_validate(
        {"Ticket": _valid_ticket(), "Article": _valid_article(), "Attachment": None}
    )
    assert payload_none.to_dict().get("Attachment") is None


def test_ticket_update_ticket_optional_non_empty():
    TicketUpdateTicket.model_validate({"Title": "New Title"})
    with pytest.raises(ValidationError):
        TicketUpdateTicket.model_validate({"Title": "   "})

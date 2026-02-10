from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.pyznuny.ticket.models import (
    Endpoint,
    TicketCreateTicket,
    TicketCreateArticle,
    TicketCreatePayload,
)


class TestEndpoint:
    """Test suite for Endpoint model"""

    def test_endpoint_creation(self):
        """Test creating a valid endpoint"""
        endpoint = Endpoint(name="test", method="GET", path="/test")
        assert endpoint.name == "test"
        assert endpoint.method == "GET"
        assert endpoint.path == "/test"

    def test_endpoint_full_path_with_base(self):
        """Test full_path with base path"""
        endpoint = Endpoint(name="test", method="GET", path="/test")
        assert endpoint.full_path("/api/v1") == "/api/v1/test"

    def test_endpoint_invalid_method(self):
        """Test creating endpoint with invalid HTTP method"""
        with pytest.raises(ValidationError):
            Endpoint(name="test", method="INVALID", path="/test")


class TestTicketCreateTicket:
    """Test suite for TicketCreateTicket model"""

    def test_ticket_create_minimal(self):
        """Test creating ticket with minimal required fields"""
        ticket = TicketCreateTicket(
            Title="Test Ticket",
            Queue="Support",
            State="new",
            Priority="3 normal"
        )
        assert ticket.Title == "Test Ticket"
        assert ticket.Queue == "Support"

    def test_ticket_validate_required_fields(self):
        """Test validate fails with empty required fields"""
        ticket = TicketCreateTicket(Title="", Queue="Support", State="new", Priority="normal")
        with pytest.raises(ValueError, match="Ticket.Title is required"):
            ticket.validate()

    def test_ticket_to_dict(self):
        """Test to_dict method"""
        ticket = TicketCreateTicket(
            Title="Test",
            Queue="Support",
            State="new",
            Priority="normal"
        )
        result = ticket.to_dict()
        assert result["Title"] == "Test"
        assert result["Queue"] == "Support"


class TestTicketCreateArticle:
    """Test suite for TicketCreateArticle model"""

    def test_article_create_minimal(self):
        """Test creating article with minimal fields"""
        article = TicketCreateArticle(
            Subject="Test Subject",
            Body="Test Body",
            ContentType="text/plain"
        )
        assert article.Subject == "Test Subject"
        assert article.Body == "Test Body"

    def test_article_validate_required_fields(self):
        """Test validate fails with empty required fields"""
        article = TicketCreateArticle(Subject="", Body="Body", ContentType="text/plain")
        with pytest.raises(ValueError, match="Article.Subject is required"):
            article.validate()

    def test_article_to_dict(self):
        """Test to_dict method"""
        article = TicketCreateArticle(
            Subject="Test",
            Body="Body",
            ContentType="text/plain"
        )
        result = article.to_dict()
        assert result["Subject"] == "Test"
        assert result["Body"] == "Body"


class TestTicketCreatePayload:
    """Test suite for TicketCreatePayload model"""

    def test_payload_create(self):
        """Test creating payload"""
        ticket = TicketCreateTicket(
            Title="Test",
            Queue="Support",
            State="new",
            Priority="normal"
        )
        article = TicketCreateArticle(
            Subject="Test",
            Body="Body",
            ContentType="text/plain"
        )
        payload = TicketCreatePayload(Ticket=ticket, Article=article)
        assert payload.Ticket == ticket
        assert payload.Article == article

    def test_payload_to_dict(self):
        """Test to_dict method"""
        ticket = TicketCreateTicket(
            Title="Test",
            Queue="Support",
            State="new",
            Priority="normal"
        )
        article = TicketCreateArticle(
            Subject="Test",
            Body="Body",
            ContentType="text/plain"
        )
        payload = TicketCreatePayload(Ticket=ticket, Article=article)
        result = payload.to_dict()

        assert "Ticket" in result
        assert "Article" in result
        assert result["Ticket"]["Title"] == "Test"

from __future__ import annotations

from unittest.mock import Mock, patch

import httpx

from src.pyznuny.ticket.client import TicketClient
from src.pyznuny.ticket.models import (
    TicketCreateArticle,
    TicketCreatePayload,
    TicketCreateTicket,
)
from src.pyznuny.ticket.routes import SessionRoutes, TicketRoutes


class TestSessionRoutes:
    """Test suite for SessionRoutes class"""

    def test_create_session(self):
        """Test creating a session"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"SessionID": "test-session-id"}

        with (patch.object(TicketClient, 'request', return_value=mock_response)
              as mock_request):
            client = TicketClient(base_url="https://api.example.com")
            session_routes = SessionRoutes(client)

            response = session_routes.create("testuser", "testpass")

            mock_request.assert_called_once_with(
                "session_create",
                json={"UserLogin": "testuser", "Password": "testpass"}
            )
            assert response == mock_response
            client.close()


class TestTicketRoutes:
    """Test suite for TicketRoutes class"""

    def test_create_ticket(self):
        """Test creating ticket with payload object"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"TicketID": "123"}

        ticket = TicketCreateTicket(
            Title="Test Ticket",
            Queue="Support",
            State="new",
            Priority="normal",
            CustomerUser="customer@example.com"
        )
        article = TicketCreateArticle(
            Subject="Test Subject",
            Body="Test Body",
            ContentType="text/plain"
        )
        payload = TicketCreatePayload(Ticket=ticket, Article=article)

        with (patch.object(TicketClient, 'request', return_value=mock_response)
              as mock_request):
            client = TicketClient(base_url="https://api.example.com")
            client.session_id = "test-session-id"
            ticket_routes = TicketRoutes(client)

            ticket_routes.create(payload)

            args, kwargs = mock_request.call_args
            assert args[0] == "ticket_create"
            assert "SessionID" in kwargs["json"]
            assert "Ticket" in kwargs["json"]
            assert "Article" in kwargs["json"]
            client.close()

    def test_update_ticket(self):
        """Test updating a ticket"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"TicketID": "123"}

        with (patch.object(TicketClient, 'request', return_value=mock_response)
              as mock_request):
            client = TicketClient(base_url="https://api.example.com")
            client.session_id = "test-session-id"
            ticket_routes = TicketRoutes(client)
            ticket_routes.update("123", Ticket={"Title": "Updated Title"})

            args, kwargs = mock_request.call_args
            assert args[0] == "ticket_update"
            assert kwargs["path_params"]["ticket_id"] == "123"
            assert kwargs["json"]["Ticket"]["Title"] == "Updated Title"
            client.close()

    def test_get_ticket(self):
        """Test getting a ticket"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"Ticket": [
            {"TicketID": "123",
             "Title": "Test"}]
        }

        with (patch.object(TicketClient, 'request', return_value=mock_response)
              as mock_request):
            client = TicketClient(base_url="https://api.example.com")
            client.session_id = "test-session-id"
            ticket_routes = TicketRoutes(client)

            ticket_routes.get("123")

            args, kwargs = mock_request.call_args
            assert args[0] == "ticket_get"
            assert kwargs["path_params"]["ticket_id"] == "123"
            assert kwargs["params"]["SessionID"] == "test-session-id"
            client.close()

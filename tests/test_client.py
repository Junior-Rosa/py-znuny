from __future__ import annotations

from unittest.mock import Mock, patch

import httpx
import pytest

from src.pyznuny.ticket.client import TicketClient
from src.pyznuny.ticket.exceptions import TicketClientError


class TestTicketClient:
    """Test suite for TicketClient class"""

    def test_init_with_base_url(self):
        """Test client initialization with base URL"""
        client = TicketClient(base_url="https://api.example.com")
        assert client._client.base_url == "https://api.example.com"
        client.close()

    def test_login(self):
        """Test login method"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"SessionID": "test-session-id"}

        with patch.object(TicketClient, 'request', return_value=mock_response):
            client = TicketClient(base_url="https://api.example.com")
            client.login("testuser", "testpass")
            assert client.session_id == "test-session-id"
            client.close()

    def test_request_basic(self):
        """Test basic request method"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()

        with patch.object(httpx.Client, 'request', return_value=mock_response):
            client = TicketClient(base_url="https://api.example.com")
            response = client.request("session_create", json={"test": "data"})
            assert response == mock_response
            client.close()

    def test_request_with_path_params(self):
        """Test request with path parameters"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()

        with (patch.object(httpx.Client, 'request', return_value=mock_response)
              as mock_request):
            client = TicketClient(base_url="https://api.example.com")
            client.request("ticket_get", path_params={"ticket_id": "123"})
            call_args = mock_request.call_args
            assert "123" in call_args[0][1]
            client.close()

    def test_request_error_handling(self):
        """Test request handling API errors"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "Error": {"ErrorCode": "400", "ErrorMessage": "Bad Request"}
        }

        with patch.object(httpx.Client, 'request', return_value=mock_response):
            client = TicketClient(base_url="https://api.example.com")
            with pytest.raises(TicketClientError):
                client.request("session_create")
            client.close()

    def test_context_manager(self):
        """Test client as context manager"""
        with TicketClient(base_url="https://api.example.com") as client:
            assert isinstance(client, TicketClient)

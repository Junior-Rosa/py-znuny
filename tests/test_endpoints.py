from __future__ import annotations

import pytest

from src.pyznuny.ticket.client import TicketClient
from src.pyznuny.ticket.endpoints import EndpointSetter, EndpointsRegistry
from src.pyznuny.ticket.models import Endpoint


class TestEndpointsRegistry:
    """Test suite for EndpointsRegistry class"""

    def test_register_and_get_endpoint(self):
        """Test registering and retrieving an endpoint"""
        registry = EndpointsRegistry()
        endpoint = Endpoint(name="test", method="GET", path="/test")
        registry.register(endpoint)
        assert registry.get("test") == endpoint

    def test_path_for_with_base_path(self):
        """Test path_for with base path"""
        registry = EndpointsRegistry(base_path="/api/v1")
        endpoint = Endpoint(name="test", method="GET", path="/test")
        registry.register(endpoint)
        assert registry.path_for("test") == "/api/v1/test"

    def test_get_endpoint_not_found(self):
        """Test getting non-existent endpoint raises KeyError"""
        registry = EndpointsRegistry()
        with pytest.raises(KeyError):
            registry.get("nonexistent")


class TestEndpointSetter:
    """Test suite for EndpointSetter class"""

    def test_ticket_create_endpoint(self):
        """Test setting ticket_create endpoint"""
        client = TicketClient()
        setter = EndpointSetter(client)
        endpoint = setter.ticket_create(endpoint="/custom/ticket")
        assert endpoint.name == "ticket_create"
        assert endpoint.method == "POST"
        client.close()

    def test_ticket_get_endpoint(self):
        """Test setting ticket_get endpoint"""
        client = TicketClient()
        setter = EndpointSetter(client)
        endpoint = setter.ticket_get(endpoint="/custom/ticket/{id}", identifier="id")
        assert endpoint.name == "ticket_get"
        assert client.endpoint_identifier("ticket_get") == "id"
        client.close()

    def test_ticket_update_endpoint(self):
        """Test setting ticket_update endpoint"""
        client = TicketClient()
        setter = EndpointSetter(client)
        endpoint = setter.ticket_update(endpoint="/custom/ticket/{id}", identifier="id")
        assert endpoint.name == "ticket_update"
        assert client.endpoint_identifier("ticket_update") == "id"
        client.close()


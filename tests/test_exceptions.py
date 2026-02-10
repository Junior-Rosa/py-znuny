from __future__ import annotations

import pytest

from src.pyznuny.ticket.exceptions import TicketClientError


class TestTicketClientError:
    """Test suite for TicketClientError exception"""

    def test_error_message_format_with_code_and_message(self):
        """Test error message format when both code and message present"""
        error_dict = {
            "ErrorCode": "400",
            "ErrorMessage": "Bad Request"
        }
        error = TicketClientError(error_dict)
        assert str(error) == "400: Bad Request"

    def test_error_message_format_with_message_only(self):
        """Test error message format when only message present"""
        error_dict = {
            "ErrorMessage": "Invalid input"
        }
        error = TicketClientError(error_dict)
        assert str(error) == "Invalid input"

    def test_error_with_string(self):
        """Test error creation with string error"""
        error = TicketClientError("Connection timeout")
        assert str(error) == "Connection timeout: Connection timeout"

    def test_error_can_be_raised(self):
        """Test that error can be raised and caught"""
        error_dict = {
            "ErrorCode": "403",
            "ErrorMessage": "Forbidden"
        }
        with pytest.raises(TicketClientError):
            raise TicketClientError(error_dict)
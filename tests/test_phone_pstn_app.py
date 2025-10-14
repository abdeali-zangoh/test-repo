"""Tests for phone-pstn-app/main.py"""
import json
import os
import sys
import tempfile
from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest

# Add phone-pstn-app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phone-pstn-app"))

from main import PhonePSTNApp, main


class TestPhonePSTNApp:
    """Test PhonePSTNApp class"""

    def setup_method(self):
        """Setup test fixtures"""
        self.temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
        self.temp_file.close()
        self.app = PhonePSTNApp(data_file=self.temp_file.name)

    def teardown_method(self):
        """Cleanup test fixtures"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_init_creates_empty_calls_list(self):
        """Test that initialization creates an empty calls list"""
        assert self.app.calls == []
        assert self.app.data_file == self.temp_file.name

    def test_load_calls_empty_file(self):
        """Test loading calls from non-existent file"""
        calls = self.app.load_calls()
        assert calls == []

    def test_load_calls_with_data(self):
        """Test loading calls from file with data"""
        test_data = [
            {
                "id": 1,
                "phone_number": "+1234567890",
                "contact_name": "John",
                "timestamp": "2024-01-01T10:00:00",
                "duration": 120,
                "status": "completed",
            }
        ]
        with open(self.temp_file.name, "w") as f:
            json.dump(test_data, f)

        app = PhonePSTNApp(data_file=self.temp_file.name)
        assert len(app.calls) == 1
        assert app.calls[0]["phone_number"] == "+1234567890"

    def test_load_calls_invalid_json(self):
        """Test loading calls from file with invalid JSON"""
        with open(self.temp_file.name, "w") as f:
            f.write("invalid json{")

        app = PhonePSTNApp(data_file=self.temp_file.name)
        assert app.calls == []

    def test_save_calls(self):
        """Test saving calls to file"""
        self.app.calls = [
            {
                "id": 1,
                "phone_number": "+1234567890",
                "contact_name": "Jane",
                "timestamp": "2024-01-01T10:00:00",
                "duration": 60,
                "status": "completed",
            }
        ]
        self.app.save_calls()

        with open(self.temp_file.name, "r") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["phone_number"] == "+1234567890"

    def test_make_call_valid_number(self):
        """Test making a call with valid phone number"""
        call = self.app.make_call("+1234567890", "Alice")
        assert call["id"] == 1
        assert call["phone_number"] == "+1234567890"
        assert call["contact_name"] == "Alice"
        assert call["status"] == "initiated"
        assert call["duration"] == 0
        assert len(self.app.calls) == 1

    def test_make_call_invalid_number(self):
        """Test making a call with invalid phone number"""
        with pytest.raises(ValueError, match="Invalid phone number format"):
            self.app.make_call("123")

    def test_make_call_without_contact_name(self):
        """Test making a call without contact name"""
        call = self.app.make_call("+1234567890")
        assert call["contact_name"] == ""

    def test_end_call_success(self):
        """Test ending a call successfully"""
        call = self.app.make_call("+1234567890", "Bob")
        result = self.app.end_call(call["id"], 180)
        assert result is True
        assert self.app.calls[0]["duration"] == 180
        assert self.app.calls[0]["status"] == "completed"

    def test_end_call_not_found(self):
        """Test ending a non-existent call"""
        result = self.app.end_call(999, 100)
        assert result is False

    def test_validate_phone_number_valid(self):
        """Test phone number validation with valid numbers"""
        assert self.app.validate_phone_number("+1234567890") is True
        assert self.app.validate_phone_number("123-456-7890") is True
        assert self.app.validate_phone_number("(123) 456-7890") is True
        assert self.app.validate_phone_number("12345678901") is True

    def test_validate_phone_number_invalid(self):
        """Test phone number validation with invalid numbers"""
        assert self.app.validate_phone_number("123") is False
        assert self.app.validate_phone_number("abc") is False
        assert self.app.validate_phone_number("") is False

    def test_get_call_history(self):
        """Test getting call history"""
        self.app.make_call("+1234567890", "Charlie")
        self.app.make_call("+0987654321", "Diana")
        history = self.app.get_call_history()
        assert len(history) == 2
        assert history[0]["contact_name"] == "Charlie"
        assert history[1]["contact_name"] == "Diana"

    def test_search_calls_by_phone_number(self):
        """Test searching calls by phone number"""
        self.app.make_call("+1234567890", "Eve")
        self.app.make_call("+0987654321", "Frank")
        results = self.app.search_calls("123")
        assert len(results) == 1
        assert results[0]["contact_name"] == "Eve"

    def test_search_calls_by_contact_name(self):
        """Test searching calls by contact name"""
        self.app.make_call("+1234567890", "Grace")
        self.app.make_call("+0987654321", "Henry")
        results = self.app.search_calls("grace")
        assert len(results) == 1
        assert results[0]["phone_number"] == "+1234567890"

    def test_search_calls_no_results(self):
        """Test searching calls with no matches"""
        self.app.make_call("+1234567890", "Ivy")
        results = self.app.search_calls("xyz")
        assert len(results) == 0

    def test_get_call_stats_empty(self):
        """Test getting stats with no calls"""
        stats = self.app.get_call_stats()
        assert stats["total_calls"] == 0
        assert stats["completed_calls"] == 0
        assert stats["total_duration_seconds"] == 0
        assert stats["average_duration"] == 0

    def test_get_call_stats_with_calls(self):
        """Test getting stats with calls"""
        call1 = self.app.make_call("+1234567890", "Jack")
        self.app.end_call(call1["id"], 120)
        call2 = self.app.make_call("+0987654321", "Kate")
        self.app.end_call(call2["id"], 180)

        stats = self.app.get_call_stats()
        assert stats["total_calls"] == 2
        assert stats["completed_calls"] == 2
        assert stats["total_duration_seconds"] == 300
        assert stats["average_duration"] == 150

    def test_get_call_stats_mixed_status(self):
        """Test getting stats with mixed call statuses"""
        call1 = self.app.make_call("+1234567890", "Leo")
        self.app.end_call(call1["id"], 60)
        self.app.make_call("+0987654321", "Mia")  # Not ended

        stats = self.app.get_call_stats()
        assert stats["total_calls"] == 2
        assert stats["completed_calls"] == 1
        assert stats["average_duration"] == 60


class TestMain:
    """Test main function"""

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_exit_immediately(self, mock_print, mock_input):
        """Test main function exits on choice 6"""
        mock_input.return_value = "6"
        main()
        # Verify exit message was printed
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Goodbye!" in call for call in calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_invalid_choice(self, mock_print, mock_input):
        """Test main function handles invalid choice"""
        mock_input.side_effect = ["99", "6"]
        main()
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Invalid choice" in call for call in calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_keyboard_interrupt(self, mock_print, mock_input):
        """Test main function handles keyboard interrupt"""
        mock_input.side_effect = KeyboardInterrupt()
        main()
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Goodbye!" in call for call in calls)

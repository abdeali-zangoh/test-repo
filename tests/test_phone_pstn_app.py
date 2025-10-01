#!/usr/bin/env python3
"""Tests for Phone PSTN Application"""

import json
import os
import tempfile
from datetime import datetime
import pytest
from src.phone_pstn_app.main import PhonePSTNApp


class TestPhonePSTNApp:
    """Test cases for PhonePSTNApp class"""

    @pytest.fixture
    def temp_data_file(self):
        """Create a temporary data file for testing"""
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @pytest.fixture
    def app(self, temp_data_file):
        """Create a PhonePSTNApp instance with temporary data file"""
        return PhonePSTNApp(data_file=temp_data_file)

    def test_init_creates_empty_calls_list(self, temp_data_file):
        """Test that initialization creates an empty calls list"""
        app = PhonePSTNApp(data_file=temp_data_file)
        assert app.calls == []
        assert app.data_file == temp_data_file

    def test_load_calls_with_nonexistent_file(self, temp_data_file):
        """Test loading calls when file doesn't exist"""
        os.unlink(temp_data_file)
        app = PhonePSTNApp(data_file=temp_data_file)
        assert app.calls == []

    def test_load_calls_with_valid_data(self, temp_data_file):
        """Test loading calls from existing file with valid data"""
        test_data = [
            {
                "id": 1,
                "phone_number": "+1234567890",
                "contact_name": "John Doe",
                "timestamp": "2024-01-01T10:00:00",
                "duration": 120,
                "status": "completed"
            }
        ]
        with open(temp_data_file, 'w') as f:
            json.dump(test_data, f)

        app = PhonePSTNApp(data_file=temp_data_file)
        assert len(app.calls) == 1
        assert app.calls[0]["phone_number"] == "+1234567890"

    def test_load_calls_with_invalid_json(self, temp_data_file):
        """Test loading calls from file with invalid JSON"""
        with open(temp_data_file, 'w') as f:
            f.write("invalid json content")

        app = PhonePSTNApp(data_file=temp_data_file)
        assert app.calls == []

    def test_save_calls(self, app, temp_data_file):
        """Test saving calls to file"""
        app.calls = [
            {
                "id": 1,
                "phone_number": "+1234567890",
                "contact_name": "Test",
                "timestamp": "2024-01-01T10:00:00",
                "duration": 60,
                "status": "completed"
            }
        ]
        app.save_calls()

        with open(temp_data_file, 'r') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["phone_number"] == "+1234567890"

    def test_validate_phone_number_valid(self, app):
        """Test phone number validation with valid numbers"""
        valid_numbers = [
            "+1234567890",
            "1234567890",
            "(123) 456-7890",
            "+1 (234) 567-8900",
            "123-456-7890"
        ]
        for number in valid_numbers:
            assert app.validate_phone_number(number) is True

    def test_validate_phone_number_invalid(self, app):
        """Test phone number validation with invalid numbers"""
        invalid_numbers = [
            "123",
            "12345",
            "abc",
            "",
            "123-456"
        ]
        for number in invalid_numbers:
            assert app.validate_phone_number(number) is False

    def test_make_call_valid(self, app):
        """Test making a call with valid phone number"""
        result = app.make_call("+1234567890", "John Doe")

        assert result["id"] == 1
        assert result["phone_number"] == "+1234567890"
        assert result["contact_name"] == "John Doe"
        assert result["duration"] == 0
        assert result["status"] == "initiated"
        assert "timestamp" in result
        assert len(app.calls) == 1

    def test_make_call_without_contact_name(self, app):
        """Test making a call without contact name"""
        result = app.make_call("+1234567890")

        assert result["contact_name"] == ""
        assert result["phone_number"] == "+1234567890"

    def test_make_call_invalid_phone_number(self, app):
        """Test making a call with invalid phone number"""
        with pytest.raises(ValueError, match="Invalid phone number format"):
            app.make_call("123")

    def test_make_call_increments_id(self, app):
        """Test that call IDs increment correctly"""
        call1 = app.make_call("+1234567890")
        call2 = app.make_call("+0987654321")

        assert call1["id"] == 1
        assert call2["id"] == 2

    def test_end_call_success(self, app):
        """Test ending a call successfully"""
        call = app.make_call("+1234567890")
        result = app.end_call(call["id"], 120)

        assert result is True
        assert app.calls[0]["duration"] == 120
        assert app.calls[0]["status"] == "completed"

    def test_end_call_not_found(self, app):
        """Test ending a call that doesn't exist"""
        result = app.end_call(999, 120)
        assert result is False

    def test_get_call_history_empty(self, app):
        """Test getting call history when empty"""
        history = app.get_call_history()
        assert history == []

    def test_get_call_history_with_calls(self, app):
        """Test getting call history with existing calls"""
        app.make_call("+1234567890", "John")
        app.make_call("+0987654321", "Jane")

        history = app.get_call_history()
        assert len(history) == 2
        assert history[0]["contact_name"] == "John"
        assert history[1]["contact_name"] == "Jane"

    def test_search_calls_by_phone_number(self, app):
        """Test searching calls by phone number"""
        app.make_call("+1234567890", "John")
        app.make_call("+0987654321", "Jane")

        results = app.search_calls("1234")
        assert len(results) == 1
        assert results[0]["phone_number"] == "+1234567890"

    def test_search_calls_by_contact_name(self, app):
        """Test searching calls by contact name"""
        app.make_call("+1234567890", "John Doe")
        app.make_call("+0987654321", "Jane Smith")

        results = app.search_calls("john")
        assert len(results) == 1
        assert results[0]["contact_name"] == "John Doe"

    def test_search_calls_case_insensitive(self, app):
        """Test that search is case insensitive"""
        app.make_call("+1234567890", "John Doe")

        results = app.search_calls("JOHN")
        assert len(results) == 1
        assert results[0]["contact_name"] == "John Doe"

    def test_search_calls_no_results(self, app):
        """Test searching with no matching results"""
        app.make_call("+1234567890", "John")

        results = app.search_calls("nonexistent")
        assert results == []

    def test_get_call_stats_empty(self, app):
        """Test getting stats with no calls"""
        stats = app.get_call_stats()

        assert stats["total_calls"] == 0
        assert stats["completed_calls"] == 0
        assert stats["total_duration_seconds"] == 0
        assert stats["average_duration"] == 0

    def test_get_call_stats_with_calls(self, app):
        """Test getting stats with completed calls"""
        call1 = app.make_call("+1234567890")
        call2 = app.make_call("+0987654321")
        app.end_call(call1["id"], 120)
        app.end_call(call2["id"], 180)

        stats = app.get_call_stats()

        assert stats["total_calls"] == 2
        assert stats["completed_calls"] == 2
        assert stats["total_duration_seconds"] == 300
        assert stats["average_duration"] == 150

    def test_get_call_stats_mixed_status(self, app):
        """Test getting stats with mixed call statuses"""
        call1 = app.make_call("+1234567890")
        call2 = app.make_call("+0987654321")
        app.end_call(call1["id"], 120)
        # call2 remains initiated

        stats = app.get_call_stats()

        assert stats["total_calls"] == 2
        assert stats["completed_calls"] == 1
        assert stats["total_duration_seconds"] == 120
        assert stats["average_duration"] == 120

    def test_data_persistence(self, temp_data_file):
        """Test that data persists across app instances"""
        app1 = PhonePSTNApp(data_file=temp_data_file)
        app1.make_call("+1234567890", "John")

        app2 = PhonePSTNApp(data_file=temp_data_file)
        assert len(app2.calls) == 1
        assert app2.calls[0]["contact_name"] == "John"

    def test_search_calls_with_empty_contact_name(self, app):
        """Test searching calls where contact_name might be missing"""
        app.make_call("+1234567890", "John")
        app.make_call("+0987654321")  # No contact name

        results = app.search_calls("098")
        assert len(results) == 1
        assert results[0]["phone_number"] == "+0987654321"

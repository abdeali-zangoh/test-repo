"""Tests for to-do-app/todo.py"""
import json
import os
import sys
import tempfile
from datetime import datetime
from unittest.mock import patch

import pytest

# Add to-do-app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "to-do-app"))

from todo import TodoApp, print_help, main


class TestTodoApp:
    """Test TodoApp class"""

    def setup_method(self):
        """Setup test fixtures"""
        self.temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
        self.temp_file.close()
        self.app = TodoApp(data_file=self.temp_file.name)

    def teardown_method(self):
        """Cleanup test fixtures"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_init_creates_empty_tasks_list(self):
        """Test that initialization creates an empty tasks list"""
        assert self.app.tasks == []
        assert self.app.data_file == self.temp_file.name

    def test_load_tasks_empty_file(self):
        """Test loading tasks from non-existent file"""
        tasks = self.app.load_tasks()
        assert tasks == []

    def test_load_tasks_with_data(self):
        """Test loading tasks from file with data"""
        test_data = [
            {
                "id": 1,
                "description": "Test task",
                "completed": False,
                "created_at": "2024-01-01T10:00:00",
                "completed_at": None,
            }
        ]
        with open(self.temp_file.name, "w") as f:
            json.dump(test_data, f)

        app = TodoApp(data_file=self.temp_file.name)
        assert len(app.tasks) == 1
        assert app.tasks[0]["description"] == "Test task"

    def test_load_tasks_invalid_json(self):
        """Test loading tasks from file with invalid JSON"""
        with open(self.temp_file.name, "w") as f:
            f.write("invalid json{")

        app = TodoApp(data_file=self.temp_file.name)
        assert app.tasks == []

    def test_save_tasks(self):
        """Test saving tasks to file"""
        self.app.tasks = [
            {
                "id": 1,
                "description": "Save test",
                "completed": False,
                "created_at": "2024-01-01T10:00:00",
                "completed_at": None,
            }
        ]
        self.app.save_tasks()

        with open(self.temp_file.name, "r") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["description"] == "Save test"

    @patch("builtins.print")
    def test_add_task(self, mock_print):
        """Test adding a new task"""
        self.app.add_task("Buy groceries")
        assert len(self.app.tasks) == 1
        assert self.app.tasks[0]["description"] == "Buy groceries"
        assert self.app.tasks[0]["completed"] is False
        assert self.app.tasks[0]["id"] == 1
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_add_multiple_tasks(self, mock_print):
        """Test adding multiple tasks"""
        self.app.add_task("Task 1")
        self.app.add_task("Task 2")
        assert len(self.app.tasks) == 2
        assert self.app.tasks[1]["id"] == 2

    @patch("builtins.print")
    def test_list_tasks_empty(self, mock_print):
        """Test listing tasks when list is empty"""
        self.app.list_tasks()
        mock_print.assert_called_with("No tasks found.")

    @patch("builtins.print")
    def test_list_tasks_with_tasks(self, mock_print):
        """Test listing tasks"""
        self.app.add_task("Task 1")
        self.app.add_task("Task 2")
        self.app.list_tasks()
        # Verify that print was called multiple times
        assert mock_print.call_count > 2

    @patch("builtins.print")
    def test_list_tasks_hide_completed(self, mock_print):
        """Test listing tasks hides completed by default"""
        self.app.add_task("Task 1")
        self.app.tasks[0]["completed"] = True
        self.app.list_tasks(show_completed=False)
        # Task should not be shown
        calls = [str(call) for call in mock_print.call_args_list]
        task_shown = any("Task 1" in call for call in calls)
        assert not task_shown

    @patch("builtins.print")
    def test_list_tasks_show_completed(self, mock_print):
        """Test listing tasks shows completed when requested"""
        self.app.add_task("Task 1")
        self.app.tasks[0]["completed"] = True
        self.app.tasks[0]["completed_at"] = datetime.now().isoformat()
        self.app.list_tasks(show_completed=True)
        # Task should be shown
        calls = [str(call) for call in mock_print.call_args_list]
        task_shown = any("Task 1" in call for call in calls)
        assert task_shown

    @patch("builtins.print")
    def test_complete_task_success(self, mock_print):
        """Test completing a task"""
        self.app.add_task("Task to complete")
        self.app.complete_task(1)
        assert self.app.tasks[0]["completed"] is True
        assert self.app.tasks[0]["completed_at"] is not None

    @patch("builtins.print")
    def test_complete_task_already_completed(self, mock_print):
        """Test completing an already completed task"""
        self.app.add_task("Already done")
        self.app.tasks[0]["completed"] = True
        self.app.complete_task(1)
        # Should print message about already completed
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("already completed" in call for call in calls)

    @patch("builtins.print")
    def test_complete_task_not_found(self, mock_print):
        """Test completing a non-existent task"""
        self.app.complete_task(999)
        mock_print.assert_called_with("Task 999 not found.")

    @patch("builtins.print")
    def test_delete_task_success(self, mock_print):
        """Test deleting a task"""
        self.app.add_task("Task to delete")
        self.app.delete_task(1)
        assert len(self.app.tasks) == 0

    @patch("builtins.print")
    def test_delete_task_not_found(self, mock_print):
        """Test deleting a non-existent task"""
        self.app.delete_task(999)
        mock_print.assert_called_with("Task 999 not found.")

    @patch("builtins.print")
    def test_clear_completed(self, mock_print):
        """Test clearing completed tasks"""
        self.app.add_task("Task 1")
        self.app.add_task("Task 2")
        self.app.add_task("Task 3")
        self.app.tasks[0]["completed"] = True
        self.app.tasks[1]["completed"] = True

        self.app.clear_completed()
        assert len(self.app.tasks) == 1
        assert self.app.tasks[0]["description"] == "Task 3"


class TestPrintHelp:
    """Test print_help function"""

    @patch("builtins.print")
    def test_print_help(self, mock_print):
        """Test print_help displays help message"""
        print_help()
        mock_print.assert_called_once()
        help_text = str(mock_print.call_args[0][0])
        assert "Usage:" in help_text
        assert "Commands:" in help_text


class TestMain:
    """Test main function"""

    @patch("sys.argv", ["todo.py"])
    @patch("builtins.print")
    def test_main_no_args(self, mock_print):
        """Test main with no arguments shows help"""
        main()
        help_text = str(mock_print.call_args[0][0])
        assert "Usage:" in help_text

    @patch("sys.argv", ["todo.py", "help"])
    @patch("builtins.print")
    def test_main_help_command(self, mock_print):
        """Test main with help command"""
        main()
        help_text = str(mock_print.call_args[0][0])
        assert "Usage:" in help_text

    @patch("sys.argv", ["todo.py", "add"])
    @patch("builtins.print")
    def test_main_add_without_description(self, mock_print):
        """Test main add command without description"""
        main()
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Error:" in call for call in calls)

    @patch("sys.argv", ["todo.py", "complete"])
    @patch("builtins.print")
    def test_main_complete_without_id(self, mock_print):
        """Test main complete command without ID"""
        main()
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Error:" in call for call in calls)

    @patch("sys.argv", ["todo.py", "complete", "abc"])
    @patch("builtins.print")
    def test_main_complete_invalid_id(self, mock_print):
        """Test main complete command with invalid ID"""
        main()
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Error:" in call for call in calls)

    @patch("sys.argv", ["todo.py", "delete"])
    @patch("builtins.print")
    def test_main_delete_without_id(self, mock_print):
        """Test main delete command without ID"""
        main()
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Error:" in call for call in calls)

    @patch("sys.argv", ["todo.py", "delete", "xyz"])
    @patch("builtins.print")
    def test_main_delete_invalid_id(self, mock_print):
        """Test main delete command with invalid ID"""
        main()
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Error:" in call for call in calls)

    @patch("sys.argv", ["todo.py", "unknown"])
    @patch("builtins.print")
    def test_main_unknown_command(self, mock_print):
        """Test main with unknown command"""
        main()
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Unknown command:" in call for call in calls)

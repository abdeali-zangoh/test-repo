#!/usr/bin/env python3
"""Tests for To-Do Task Application"""

import json
import os
import tempfile
from datetime import datetime
import pytest
from unittest.mock import patch, call
from src.todo_app.todo import TodoApp, print_help, main


class TestTodoApp:
    """Test cases for TodoApp class"""

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
        """Create a TodoApp instance with temporary data file"""
        return TodoApp(data_file=temp_data_file)

    def test_init_creates_empty_tasks_list(self, temp_data_file):
        """Test that initialization creates an empty tasks list"""
        app = TodoApp(data_file=temp_data_file)
        assert app.tasks == []
        assert app.data_file == temp_data_file

    def test_load_tasks_with_nonexistent_file(self, temp_data_file):
        """Test loading tasks when file doesn't exist"""
        os.unlink(temp_data_file)
        app = TodoApp(data_file=temp_data_file)
        assert app.tasks == []

    def test_load_tasks_with_valid_data(self, temp_data_file):
        """Test loading tasks from existing file with valid data"""
        test_data = [
            {
                "id": 1,
                "description": "Test task",
                "completed": False,
                "created_at": "2024-01-01T10:00:00",
                "completed_at": None
            }
        ]
        with open(temp_data_file, 'w') as f:
            json.dump(test_data, f)

        app = TodoApp(data_file=temp_data_file)
        assert len(app.tasks) == 1
        assert app.tasks[0]["description"] == "Test task"

    def test_load_tasks_with_invalid_json(self, temp_data_file):
        """Test loading tasks from file with invalid JSON"""
        with open(temp_data_file, 'w') as f:
            f.write("invalid json content")

        app = TodoApp(data_file=temp_data_file)
        assert app.tasks == []

    def test_save_tasks(self, app, temp_data_file):
        """Test saving tasks to file"""
        app.tasks = [
            {
                "id": 1,
                "description": "Test task",
                "completed": False,
                "created_at": "2024-01-01T10:00:00",
                "completed_at": None
            }
        ]
        app.save_tasks()

        with open(temp_data_file, 'r') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["description"] == "Test task"

    def test_add_task(self, app, capsys):
        """Test adding a new task"""
        app.add_task("Buy groceries")

        assert len(app.tasks) == 1
        assert app.tasks[0]["description"] == "Buy groceries"
        assert app.tasks[0]["completed"] is False
        assert app.tasks[0]["id"] == 1
        assert "created_at" in app.tasks[0]

        captured = capsys.readouterr()
        assert "Added task: Buy groceries" in captured.out

    def test_add_task_increments_id(self, app):
        """Test that task IDs increment correctly"""
        app.add_task("Task 1")
        app.add_task("Task 2")

        assert app.tasks[0]["id"] == 1
        assert app.tasks[1]["id"] == 2

    def test_list_tasks_empty(self, app, capsys):
        """Test listing tasks when none exist"""
        app.list_tasks()

        captured = capsys.readouterr()
        assert "No tasks found" in captured.out

    def test_list_tasks_with_pending_tasks(self, app, capsys):
        """Test listing pending tasks"""
        app.add_task("Task 1")
        app.add_task("Task 2")

        app.list_tasks(show_completed=False)

        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert "TO-DO TASKS" in captured.out

    def test_list_tasks_hides_completed(self, app, capsys):
        """Test that list_tasks hides completed tasks by default"""
        app.add_task("Task 1")
        app.complete_task(1)
        app.add_task("Task 2")

        app.list_tasks(show_completed=False)

        captured = capsys.readouterr()
        assert "Task 2" in captured.out

    def test_list_tasks_show_all(self, app, capsys):
        """Test listing all tasks including completed"""
        app.add_task("Task 1")
        app.complete_task(1)
        app.add_task("Task 2")

        app.list_tasks(show_completed=True)

        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out

    def test_complete_task_success(self, app, capsys):
        """Test completing a task successfully"""
        app.add_task("Task 1")

        app.complete_task(1)

        assert app.tasks[0]["completed"] is True
        assert app.tasks[0]["completed_at"] is not None

        captured = capsys.readouterr()
        assert "Completed task: Task 1" in captured.out

    def test_complete_task_not_found(self, app, capsys):
        """Test completing a task that doesn't exist"""
        app.complete_task(999)

        captured = capsys.readouterr()
        assert "Task 999 not found" in captured.out

    def test_complete_task_already_completed(self, app, capsys):
        """Test completing a task that is already completed"""
        app.add_task("Task 1")
        app.complete_task(1)

        # Clear the output buffer
        capsys.readouterr()

        app.complete_task(1)

        captured = capsys.readouterr()
        assert "already completed" in captured.out

    def test_delete_task_success(self, app, capsys):
        """Test deleting a task successfully"""
        app.add_task("Task 1")
        app.add_task("Task 2")

        app.delete_task(1)

        assert len(app.tasks) == 1
        assert app.tasks[0]["description"] == "Task 2"

        captured = capsys.readouterr()
        assert "Deleted task: Task 1" in captured.out

    def test_delete_task_not_found(self, app, capsys):
        """Test deleting a task that doesn't exist"""
        app.delete_task(999)

        captured = capsys.readouterr()
        assert "Task 999 not found" in captured.out

    def test_clear_completed(self, app, capsys):
        """Test clearing completed tasks"""
        app.add_task("Task 1")
        app.add_task("Task 2")
        app.add_task("Task 3")
        app.complete_task(1)
        app.complete_task(2)

        app.clear_completed()

        assert len(app.tasks) == 1
        assert app.tasks[0]["description"] == "Task 3"

        captured = capsys.readouterr()
        assert "Removed 2 completed tasks" in captured.out

    def test_clear_completed_none(self, app, capsys):
        """Test clearing completed tasks when none exist"""
        app.add_task("Task 1")

        app.clear_completed()

        assert len(app.tasks) == 1

        captured = capsys.readouterr()
        assert "Removed 0 completed tasks" in captured.out

    def test_data_persistence(self, temp_data_file):
        """Test that data persists across app instances"""
        app1 = TodoApp(data_file=temp_data_file)
        app1.add_task("Persistent task")

        app2 = TodoApp(data_file=temp_data_file)
        assert len(app2.tasks) == 1
        assert app2.tasks[0]["description"] == "Persistent task"

    def test_completed_at_timestamp(self, app):
        """Test that completed_at is set correctly"""
        app.add_task("Task 1")

        before = datetime.now()
        app.complete_task(1)
        after = datetime.now()

        completed_at = datetime.fromisoformat(app.tasks[0]["completed_at"])
        assert before <= completed_at <= after

    def test_created_at_timestamp(self, app):
        """Test that created_at is set correctly"""
        before = datetime.now()
        app.add_task("Task 1")
        after = datetime.now()

        created_at = datetime.fromisoformat(app.tasks[0]["created_at"])
        assert before <= created_at <= after


class TestPrintHelp:
    """Test cases for print_help function"""

    def test_print_help_output(self, capsys):
        """Test that print_help displays help information"""
        print_help()

        captured = capsys.readouterr()
        assert "To-Do Task Application" in captured.out
        assert "Usage:" in captured.out
        assert "add" in captured.out
        assert "list" in captured.out
        assert "complete" in captured.out
        assert "delete" in captured.out


class TestMain:
    """Test cases for main function"""

    def test_main_no_args(self, capsys):
        """Test main function with no arguments"""
        with patch('sys.argv', ['todo.py']):
            main()

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_main_add_command(self, capsys):
        """Test main function with add command"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['todo.py', 'add', 'Test', 'task']), \
                 patch('os.path.dirname', return_value=tmpdir), \
                 patch('os.path.abspath', return_value=tmpdir):
                main()

        captured = capsys.readouterr()
        assert "Added task" in captured.out

    def test_main_add_without_description(self, capsys):
        """Test main function with add command but no description"""
        with patch('sys.argv', ['todo.py', 'add']):
            main()

        captured = capsys.readouterr()
        assert "Please provide a task description" in captured.out

    def test_main_list_command(self, capsys):
        """Test main function with list command"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['todo.py', 'list']), \
                 patch('os.path.dirname', return_value=tmpdir), \
                 patch('os.path.abspath', return_value=tmpdir):
                main()

        captured = capsys.readouterr()
        assert "No tasks found" in captured.out or "TO-DO TASKS" in captured.out

    def test_main_listall_command(self, capsys):
        """Test main function with listall command"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['todo.py', 'listall']), \
                 patch('os.path.dirname', return_value=tmpdir), \
                 patch('os.path.abspath', return_value=tmpdir):
                main()

        captured = capsys.readouterr()
        assert "No tasks found" in captured.out or "TO-DO TASKS" in captured.out

    def test_main_complete_command(self, capsys):
        """Test main function with complete command"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['todo.py', 'complete', '1']), \
                 patch('os.path.dirname', return_value=tmpdir), \
                 patch('os.path.abspath', return_value=tmpdir):
                main()

        captured = capsys.readouterr()
        assert "not found" in captured.out or "Completed task" in captured.out

    def test_main_complete_without_id(self, capsys):
        """Test main function with complete command but no ID"""
        with patch('sys.argv', ['todo.py', 'complete']):
            main()

        captured = capsys.readouterr()
        assert "Please provide a task ID" in captured.out

    def test_main_complete_invalid_id(self, capsys):
        """Test main function with complete command and invalid ID"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['todo.py', 'complete', 'abc']), \
                 patch('os.path.dirname', return_value=tmpdir), \
                 patch('os.path.abspath', return_value=tmpdir):
                main()

        captured = capsys.readouterr()
        assert "Task ID must be a number" in captured.out

    def test_main_delete_command(self, capsys):
        """Test main function with delete command"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['todo.py', 'delete', '1']), \
                 patch('os.path.dirname', return_value=tmpdir), \
                 patch('os.path.abspath', return_value=tmpdir):
                main()

        captured = capsys.readouterr()
        assert "not found" in captured.out or "Deleted task" in captured.out

    def test_main_delete_without_id(self, capsys):
        """Test main function with delete command but no ID"""
        with patch('sys.argv', ['todo.py', 'delete']):
            main()

        captured = capsys.readouterr()
        assert "Please provide a task ID" in captured.out

    def test_main_delete_invalid_id(self, capsys):
        """Test main function with delete command and invalid ID"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['todo.py', 'delete', 'xyz']), \
                 patch('os.path.dirname', return_value=tmpdir), \
                 patch('os.path.abspath', return_value=tmpdir):
                main()

        captured = capsys.readouterr()
        assert "Task ID must be a number" in captured.out

    def test_main_clear_command(self, capsys):
        """Test main function with clear command"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['todo.py', 'clear']), \
                 patch('os.path.dirname', return_value=tmpdir), \
                 patch('os.path.abspath', return_value=tmpdir):
                main()

        captured = capsys.readouterr()
        assert "Removed" in captured.out

    def test_main_help_command(self, capsys):
        """Test main function with help command"""
        with patch('sys.argv', ['todo.py', 'help']):
            main()

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_main_unknown_command(self, capsys):
        """Test main function with unknown command"""
        with patch('sys.argv', ['todo.py', 'unknown']):
            main()

        captured = capsys.readouterr()
        assert "Unknown command: unknown" in captured.out

    def test_main_case_insensitive_commands(self, capsys):
        """Test that commands are case insensitive"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['todo.py', 'LIST']), \
                 patch('os.path.dirname', return_value=tmpdir), \
                 patch('os.path.abspath', return_value=tmpdir):
                main()

        captured = capsys.readouterr()
        assert "No tasks found" in captured.out or "TO-DO TASKS" in captured.out

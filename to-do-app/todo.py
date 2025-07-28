#!/usr/bin/env python3
"""
Simple To-Do Task Application
A command-line interface for managing tasks.
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict

class TodoApp:
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks = self.load_tasks()
    
    def load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, description: str):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Added task: {description}")
    
    def list_tasks(self, show_completed: bool = False):
        """List all tasks"""
        if not self.tasks:
            print("No tasks found.")
            return
        
        print("\n" + "="*50)
        print("TO-DO TASKS")
        print("="*50)
        
        for task in self.tasks:
            if not show_completed and task['completed']:
                continue
            
            status = "✓" if task['completed'] else "○"
            print(f"{status} [{task['id']}] {task['description']}")
            if task['completed'] and task['completed_at']:
                completed_date = datetime.fromisoformat(task['completed_at']).strftime("%Y-%m-%d %H:%M")
                print(f"    Completed: {completed_date}")
        print("="*50)
    
    def complete_task(self, task_id: int):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                if task['completed']:
                    print(f"Task {task_id} is already completed.")
                else:
                    task['completed'] = True
                    task['completed_at'] = datetime.now().isoformat()
                    self.save_tasks()
                    print(f"✓ Completed task: {task['description']}")
                return
        print(f"Task {task_id} not found.")
    
    def delete_task(self, task_id: int):
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted_task = self.tasks.pop(i)
                self.save_tasks()
                print(f"✓ Deleted task: {deleted_task['description']}")
                return
        print(f"Task {task_id} not found.")
    
    def clear_completed(self):
        """Remove all completed tasks"""
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task['completed']]
        removed_count = initial_count - len(self.tasks)
        self.save_tasks()
        print(f"✓ Removed {removed_count} completed tasks.")

def print_help():
    """Print help information"""
    print("""
To-Do Task Application

Usage:
    python todo.py <command> [arguments]

Commands:
    add <description>     Add a new task
    list                  List pending tasks
    listall               List all tasks (including completed)
    complete <id>         Mark task as completed
    delete <id>           Delete a task
    clear                 Remove all completed tasks
    help                  Show this help message

Examples:
    python todo.py add "Buy groceries"
    python todo.py list
    python todo.py complete 1
    python todo.py delete 2
    """)

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    # Change to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    app = TodoApp()
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task description.")
            print("Usage: python todo.py add <description>")
            return
        description = " ".join(sys.argv[2:])
        app.add_task(description)
    
    elif command == "list":
        app.list_tasks()
    
    elif command == "listall":
        app.list_tasks(show_completed=True)
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
            print("Usage: python todo.py complete <id>")
            return
        try:
            task_id = int(sys.argv[2])
            app.complete_task(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
            print("Usage: python todo.py delete <id>")
            return
        try:
            task_id = int(sys.argv[2])
            app.delete_task(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
    
    elif command == "clear":
        app.clear_completed()
    
    elif command == "help":
        print_help()
    
    else:
        print(f"Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    main()
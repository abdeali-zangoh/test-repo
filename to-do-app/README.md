# To-Do Task Application

A simple command-line to-do task application written in Python.

## Features

- Add new tasks
- List pending and completed tasks
- Mark tasks as completed
- Delete tasks
- Clear all completed tasks
- Persistent storage using JSON

## Usage

```bash
# Add a new task
python todo.py add "Buy groceries"

# List pending tasks
python todo.py list

# List all tasks (including completed)
python todo.py listall

# Mark task as completed
python todo.py complete 1

# Delete a task
python todo.py delete 2

# Clear all completed tasks
python todo.py clear

# Show help
python todo.py help
```

## Requirements

- Python 3.6+

## Installation

No additional dependencies required. Just run the script with Python.

## Data Storage

Tasks are stored in a `tasks.json` file in the same directory as the script.
# Phone PSTN Application

A simple Python application for managing phone calls through PSTN (Public Switched Telephone Network).

## Features

- Make phone calls with phone number validation
- Track call duration and status
- Store call history in JSON format
- Search calls by phone number or contact name
- View call statistics
- Interactive command-line interface

## Usage

Run the application:

```bash
python main.py
```

## Menu Options

1. **Make a call** - Initiate a new call with phone number and optional contact name
2. **End a call** - End an active call and record its duration
3. **View call history** - Display all previous calls
4. **Search calls** - Find calls by phone number or contact name
5. **View call statistics** - Show summary statistics
6. **Exit** - Close the application

## Data Storage

Call history is stored in `calls.json` file in the same directory.

## Phone Number Validation

The application validates phone numbers to ensure they contain at least 10 digits.

## Example Call Record

```json
{
  "id": 1,
  "phone_number": "+1-555-123-4567",
  "contact_name": "John Doe",
  "timestamp": "2025-07-21T10:30:00",
  "duration": 180,
  "status": "completed"
}
```
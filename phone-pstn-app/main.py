#!/usr/bin/env python3
"""
Phone PSTN Application
A simple application for managing phone calls through PSTN (Public Switched Telephone Network)
"""

import datetime
import json
import os
from typing import Dict, List, Optional

class PhonePSTNApp:
    def __init__(self, data_file: str = "calls.json"):
        self.data_file = data_file
        self.calls = self.load_calls()
    
    def load_calls(self) -> List[Dict]:
        """Load call history from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_calls(self) -> None:
        """Save call history to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.calls, f, indent=2)
    
    def make_call(self, phone_number: str, contact_name: str = "") -> Dict:
        """Simulate making a phone call"""
        if not self.validate_phone_number(phone_number):
            raise ValueError("Invalid phone number format")
        
        call = {
            "id": len(self.calls) + 1,
            "phone_number": phone_number,
            "contact_name": contact_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "duration": 0,
            "status": "initiated"
        }
        
        self.calls.append(call)
        self.save_calls()
        return call
    
    def end_call(self, call_id: int, duration_seconds: int) -> bool:
        """End a call and update its duration"""
        for call in self.calls:
            if call["id"] == call_id:
                call["duration"] = duration_seconds
                call["status"] = "completed"
                self.save_calls()
                return True
        return False
    
    def validate_phone_number(self, phone_number: str) -> bool:
        """Basic phone number validation"""
        cleaned = ''.join(c for c in phone_number if c.isdigit() or c in '+-()')
        digits_only = ''.join(c for c in cleaned if c.isdigit())
        return len(digits_only) >= 10
    
    def get_call_history(self) -> List[Dict]:
        """Get all call history"""
        return self.calls
    
    def search_calls(self, query: str) -> List[Dict]:
        """Search calls by phone number or contact name"""
        results = []
        query_lower = query.lower()
        for call in self.calls:
            if (query_lower in call["phone_number"] or 
                query_lower in call.get("contact_name", "").lower()):
                results.append(call)
        return results
    
    def get_call_stats(self) -> Dict:
        """Get call statistics"""
        total_calls = len(self.calls)
        total_duration = sum(call.get("duration", 0) for call in self.calls)
        completed_calls = len([c for c in self.calls if c["status"] == "completed"])
        
        return {
            "total_calls": total_calls,
            "completed_calls": completed_calls,
            "total_duration_seconds": total_duration,
            "average_duration": total_duration / completed_calls if completed_calls > 0 else 0
        }

def main():
    """Main application interface"""
    app = PhonePSTNApp()
    
    while True:
        print("\n=== Phone PSTN Application ===")
        print("1. Make a call")
        print("2. End a call")
        print("3. View call history")
        print("4. Search calls")
        print("5. View call statistics")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        try:
            if choice == "1":
                phone_number = input("Enter phone number: ").strip()
                contact_name = input("Enter contact name (optional): ").strip()
                call = app.make_call(phone_number, contact_name)
                print(f"Call initiated: ID {call['id']} to {phone_number}")
                
            elif choice == "2":
                call_id = int(input("Enter call ID to end: "))
                duration = int(input("Enter call duration in seconds: "))
                if app.end_call(call_id, duration):
                    print(f"Call {call_id} ended successfully")
                else:
                    print(f"Call {call_id} not found")
                    
            elif choice == "3":
                history = app.get_call_history()
                if not history:
                    print("No call history found")
                else:
                    print(f"\n{'ID':<4} {'Phone Number':<15} {'Contact':<20} {'Status':<10} {'Duration':<10}")
                    print("-" * 70)
                    for call in history:
                        print(f"{call['id']:<4} {call['phone_number']:<15} {call.get('contact_name', ''):<20} "
                              f"{call['status']:<10} {call.get('duration', 0):<10}s")
                              
            elif choice == "4":
                query = input("Enter search query: ").strip()
                results = app.search_calls(query)
                if not results:
                    print("No matching calls found")
                else:
                    print(f"Found {len(results)} matching calls:")
                    for call in results:
                        print(f"ID {call['id']}: {call['phone_number']} - {call.get('contact_name', 'Unknown')}")
                        
            elif choice == "5":
                stats = app.get_call_stats()
                print(f"\nCall Statistics:")
                print(f"Total calls: {stats['total_calls']}")
                print(f"Completed calls: {stats['completed_calls']}")
                print(f"Total duration: {stats['total_duration_seconds']} seconds")
                print(f"Average duration: {stats['average_duration']:.1f} seconds")
                
            elif choice == "6":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please try again.")
                
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
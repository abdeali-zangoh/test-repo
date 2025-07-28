import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.questions = self.load_questions()
        self.current_question = 0
        self.score = 0
        self.quiz_started = False
        
        self.setup_ui()
        
    def load_questions(self):
        return [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct": 2
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": 1
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct": 1
            },
            {
                "question": "Who painted the Mona Lisa?",
                "options": ["Van Gogh", "Picasso", "Da Vinci", "Monet"],
                "correct": 2
            },
            {
                "question": "What is the largest ocean on Earth?",
                "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
                "correct": 3
            },
            {
                "question": "Which programming language is known for its simplicity?",
                "options": ["C++", "Python", "Assembly", "Java"],
                "correct": 1
            },
            {
                "question": "What year did World War II end?",
                "options": ["1944", "1945", "1946", "1947"],
                "correct": 1
            },
            {
                "question": "What is the chemical symbol for gold?",
                "options": ["Go", "Gd", "Au", "Ag"],
                "correct": 2
            }
        ]
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Quiz Application", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)
        
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=20)
        
        # Welcome screen
        self.welcome_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.welcome_frame.pack(expand=True, fill="both")
        
        welcome_text = tk.Label(
            self.welcome_frame,
            text="Welcome to the Quiz!\n\nTest your knowledge with our collection of questions.\nClick 'Start Quiz' to begin.",
            font=("Arial", 16),
            bg="#f0f0f0",
            fg="#666666",
            justify="center"
        )
        welcome_text.pack(expand=True)
        
        start_btn = tk.Button(
            self.welcome_frame,
            text="Start Quiz",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=30,
            pady=10,
            command=self.start_quiz,
            cursor="hand2"
        )
        start_btn.pack(pady=20)
        
        # Quiz frame (hidden initially)
        self.quiz_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.quiz_frame,
            length=600,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        
        # Question counter
        self.counter_label = tk.Label(
            self.quiz_frame,
            text="",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#666666"
        )
        self.counter_label.pack(pady=5)
        
        # Question text
        self.question_label = tk.Label(
            self.quiz_frame,
            text="",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333",
            wraplength=700,
            justify="center"
        )
        self.question_label.pack(pady=30)
        
        # Options frame
        self.options_frame = tk.Frame(self.quiz_frame, bg="#f0f0f0")
        self.options_frame.pack(pady=20)
        
        # Radio button variable
        self.selected_option = tk.IntVar()
        self.option_buttons = []
        
        # Create option buttons
        for i in range(4):
            btn = tk.Radiobutton(
                self.options_frame,
                text="",
                variable=self.selected_option,
                value=i,
                font=("Arial", 14),
                bg="#f0f0f0",
                fg="#333333",
                selectcolor="#e0e0e0",
                cursor="hand2"
            )
            btn.pack(anchor="w", pady=5, padx=20)
            self.option_buttons.append(btn)
        
        # Button frame
        self.button_frame = tk.Frame(self.quiz_frame, bg="#f0f0f0")
        self.button_frame.pack(pady=30)
        
        # Submit button
        self.submit_btn = tk.Button(
            self.button_frame,
            text="Submit Answer",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            command=self.submit_answer,
            cursor="hand2"
        )
        self.submit_btn.pack(side="left", padx=10)
        
        # Next button
        self.next_btn = tk.Button(
            self.button_frame,
            text="Next Question",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=10,
            command=self.next_question,
            cursor="hand2",
            state="disabled"
        )
        self.next_btn.pack(side="left", padx=10)
        
        # Score label
        self.score_label = tk.Label(
            self.quiz_frame,
            text="Score: 0",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#4CAF50"
        )
        self.score_label.pack(pady=10)
    
    def start_quiz(self):
        random.shuffle(self.questions)
        self.current_question = 0
        self.score = 0
        self.quiz_started = True
        
        self.welcome_frame.pack_forget()
        self.quiz_frame.pack(expand=True, fill="both")
        
        self.progress['maximum'] = len(self.questions)
        self.display_question()
    
    def display_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            
            # Update progress
            self.progress['value'] = self.current_question + 1
            self.counter_label.config(
                text=f"Question {self.current_question + 1} of {len(self.questions)}"
            )
            
            # Display question
            self.question_label.config(text=question_data["question"])
            
            # Display options
            for i, option in enumerate(question_data["options"]):
                self.option_buttons[i].config(text=f"{chr(65+i)}. {option}")
            
            # Reset selection
            self.selected_option.set(-1)
            
            # Reset buttons
            self.submit_btn.config(state="normal")
            self.next_btn.config(state="disabled")
            
            # Update score display
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.show_results()
    
    def submit_answer(self):
        if self.selected_option.get() == -1:
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        correct_answer = self.questions[self.current_question]["correct"]
        selected = self.selected_option.get()
        
        if selected == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "Great job! That's the right answer.")
        else:
            correct_text = self.questions[self.current_question]["options"][correct_answer]
            messagebox.showinfo("Incorrect", f"Sorry, the correct answer was: {correct_text}")
        
        self.submit_btn.config(state="disabled")
        
        if self.current_question < len(self.questions) - 1:
            self.next_btn.config(state="normal")
        else:
            # Last question
            self.next_btn.config(text="Show Results", state="normal")
    
    def next_question(self):
        self.current_question += 1
        
        if self.current_question < len(self.questions):
            self.display_question()
        else:
            self.show_results()
    
    def show_results(self):
        self.quiz_frame.pack_forget()
        
        # Results frame
        results_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        results_frame.pack(expand=True, fill="both")
        
        # Results title
        results_title = tk.Label(
            results_frame,
            text="Quiz Complete!",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        results_title.pack(pady=30)
        
        # Score display
        percentage = (self.score / len(self.questions)) * 100
        score_text = f"Your Score: {self.score}/{len(self.questions)} ({percentage:.1f}%)"
        
        score_label = tk.Label(
            results_frame,
            text=score_text,
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#4CAF50"
        )
        score_label.pack(pady=20)
        
        # Performance message
        if percentage >= 80:
            message = "Excellent work! 🎉"
        elif percentage >= 60:
            message = "Good job! 👍"
        elif percentage >= 40:
            message = "Not bad, keep practicing! 📚"
        else:
            message = "Keep studying and try again! 💪"
        
        message_label = tk.Label(
            results_frame,
            text=message,
            font=("Arial", 16),
            bg="#f0f0f0",
            fg="#666666"
        )
        message_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(results_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=30)
        
        # Restart button
        restart_btn = tk.Button(
            buttons_frame,
            text="Take Quiz Again",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            command=self.restart_quiz,
            cursor="hand2"
        )
        restart_btn.pack(side="left", padx=10)
        
        # Exit button
        exit_btn = tk.Button(
            buttons_frame,
            text="Exit",
            font=("Arial", 14, "bold"),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10,
            command=self.root.quit,
            cursor="hand2"
        )
        exit_btn.pack(side="left", padx=10)
    
    def restart_quiz(self):
        # Clear all frames
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Reset variables
        self.current_question = 0
        self.score = 0
        self.quiz_started = False
        
        # Recreate UI
        self.setup_ui()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
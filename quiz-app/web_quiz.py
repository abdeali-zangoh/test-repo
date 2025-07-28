#!/usr/bin/env python3
import json
import random
import webbrowser
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

class QuizData:
    def __init__(self):
        self.questions = [
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
    
    def get_questions(self):
        shuffled = self.questions.copy()
        random.shuffle(shuffled)
        return shuffled

def generate_html():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Application</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            max-width: 600px;
            width: 90%;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .header h1 {
            color: #333;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            color: #666;
            font-size: 1.1rem;
        }
        
        .welcome-screen {
            text-align: center;
            padding: 2rem 0;
        }
        
        .welcome-screen h2 {
            color: #333;
            margin-bottom: 1rem;
        }
        
        .welcome-screen p {
            color: #666;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        .quiz-screen {
            display: none;
        }
        
        .progress-container {
            margin-bottom: 2rem;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #eee;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .question-counter {
            text-align: center;
            margin: 1rem 0;
            color: #666;
            font-size: 0.9rem;
        }
        
        .question {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            border-left: 4px solid #667eea;
        }
        
        .question h3 {
            color: #333;
            font-size: 1.3rem;
            line-height: 1.4;
        }
        
        .options {
            display: grid;
            gap: 0.8rem;
            margin-bottom: 2rem;
        }
        
        .option {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
        }
        
        .option:hover {
            background: #e9ecef;
            border-color: #667eea;
        }
        
        .option.selected {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .option.correct {
            background: #4CAF50;
            color: white;
            border-color: #4CAF50;
        }
        
        .option.incorrect {
            background: #f44336;
            color: white;
            border-color: #f44336;
        }
        
        .option-letter {
            font-weight: bold;
            margin-right: 0.8rem;
            width: 1.5rem;
            height: 1.5rem;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
        }
        
        .buttons {
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            margin: 0 0.5rem;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn.next {
            background: #FF9800;
        }
        
        .btn.next:hover {
            background: #f57c00;
        }
        
        .score {
            text-align: center;
            font-size: 1.1rem;
            font-weight: 600;
            color: #4CAF50;
        }
        
        .results-screen {
            display: none;
            text-align: center;
            padding: 2rem 0;
        }
        
        .results-screen h2 {
            color: #333;
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        .final-score {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4CAF50;
            margin: 1rem 0;
        }
        
        .performance-message {
            font-size: 1.2rem;
            color: #666;
            margin: 1rem 0 2rem;
        }
        
        .restart-btn {
            background: #4CAF50;
        }
        
        .restart-btn:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Quiz App</h1>
            <p>Test your knowledge with our interactive quiz!</p>
        </div>
        
        <div id="welcomeScreen" class="welcome-screen">
            <h2>Welcome to the Quiz!</h2>
            <p>Test your knowledge with our collection of carefully crafted questions.<br>
            Each question has four options, and only one is correct.<br>
            Are you ready to challenge yourself?</p>
            <button class="btn" onclick="startQuiz()">Start Quiz</button>
        </div>
        
        <div id="quizScreen" class="quiz-screen">
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="question-counter" id="questionCounter"></div>
            </div>
            
            <div class="question">
                <h3 id="questionText"></h3>
            </div>
            
            <div class="options" id="optionsContainer"></div>
            
            <div class="buttons">
                <button class="btn" id="submitBtn" onclick="submitAnswer()" disabled>Submit Answer</button>
                <button class="btn next" id="nextBtn" onclick="nextQuestion()" disabled>Next Question</button>
            </div>
            
            <div class="score" id="scoreDisplay">Score: 0</div>
        </div>
        
        <div id="resultsScreen" class="results-screen">
            <h2>🎉 Quiz Complete!</h2>
            <div class="final-score" id="finalScore"></div>
            <div class="performance-message" id="performanceMessage"></div>
            <button class="btn restart-btn" onclick="restartQuiz()">Take Quiz Again</button>
        </div>
    </div>

    <script>
        const questions = [
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
        ];
        
        let currentQuestion = 0;
        let score = 0;
        let selectedOption = -1;
        let shuffledQuestions = [];
        
        function shuffleArray(array) {
            const shuffled = [...array];
            for (let i = shuffled.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
            }
            return shuffled;
        }
        
        function startQuiz() {
            shuffledQuestions = shuffleArray(questions);
            currentQuestion = 0;
            score = 0;
            
            document.getElementById('welcomeScreen').style.display = 'none';
            document.getElementById('quizScreen').style.display = 'block';
            document.getElementById('resultsScreen').style.display = 'none';
            
            displayQuestion();
        }
        
        function displayQuestion() {
            if (currentQuestion < shuffledQuestions.length) {
                const question = shuffledQuestions[currentQuestion];
                
                // Update progress
                const progress = ((currentQuestion + 1) / shuffledQuestions.length) * 100;
                document.getElementById('progressFill').style.width = progress + '%';
                document.getElementById('questionCounter').textContent = 
                    `Question ${currentQuestion + 1} of ${shuffledQuestions.length}`;
                
                // Display question
                document.getElementById('questionText').textContent = question.question;
                
                // Display options
                const optionsContainer = document.getElementById('optionsContainer');
                optionsContainer.innerHTML = '';
                
                question.options.forEach((option, index) => {
                    const optionDiv = document.createElement('div');
                    optionDiv.className = 'option';
                    optionDiv.onclick = () => selectOption(index);
                    
                    optionDiv.innerHTML = `
                        <div class="option-letter">${String.fromCharCode(65 + index)}</div>
                        <div>${option}</div>
                    `;
                    
                    optionsContainer.appendChild(optionDiv);
                });
                
                // Reset selection and buttons
                selectedOption = -1;
                document.getElementById('submitBtn').disabled = true;
                document.getElementById('nextBtn').disabled = true;
                document.getElementById('nextBtn').textContent = 'Next Question';
                
                // Update score display
                document.getElementById('scoreDisplay').textContent = `Score: ${score}`;
            } else {
                showResults();
            }
        }
        
        function selectOption(index) {
            // Remove previous selection
            document.querySelectorAll('.option').forEach(opt => {
                opt.classList.remove('selected');
            });
            
            // Add selection to clicked option
            document.querySelectorAll('.option')[index].classList.add('selected');
            selectedOption = index;
            
            // Enable submit button
            document.getElementById('submitBtn').disabled = false;
        }
        
        function submitAnswer() {
            if (selectedOption === -1) {
                alert('Please select an answer!');
                return;
            }
            
            const question = shuffledQuestions[currentQuestion];
            const options = document.querySelectorAll('.option');
            
            // Show correct/incorrect
            options[question.correct].classList.add('correct');
            
            if (selectedOption === question.correct) {
                score++;
            } else {
                options[selectedOption].classList.add('incorrect');
            }
            
            // Disable clicking on options
            options.forEach(opt => {
                opt.onclick = null;
                opt.style.cursor = 'default';
            });
            
            // Update buttons
            document.getElementById('submitBtn').disabled = true;
            
            if (currentQuestion < shuffledQuestions.length - 1) {
                document.getElementById('nextBtn').disabled = false;
            } else {
                document.getElementById('nextBtn').textContent = 'Show Results';
                document.getElementById('nextBtn').disabled = false;
            }
        }
        
        function nextQuestion() {
            currentQuestion++;
            
            if (currentQuestion < shuffledQuestions.length) {
                displayQuestion();
            } else {
                showResults();
            }
        }
        
        function showResults() {
            document.getElementById('quizScreen').style.display = 'none';
            document.getElementById('resultsScreen').style.display = 'block';
            
            const percentage = (score / shuffledQuestions.length) * 100;
            document.getElementById('finalScore').textContent = 
                `${score}/${shuffledQuestions.length} (${percentage.toFixed(1)}%)`;
            
            let message = '';
            if (percentage >= 80) {
                message = '🎉 Excellent work! You really know your stuff!';
            } else if (percentage >= 60) {
                message = '👍 Good job! You did well!';
            } else if (percentage >= 40) {
                message = '📚 Not bad, keep practicing!';
            } else {
                message = '💪 Keep studying and try again!';
            }
            
            document.getElementById('performanceMessage').textContent = message;
        }
        
        function restartQuiz() {
            document.getElementById('resultsScreen').style.display = 'none';
            document.getElementById('welcomeScreen').style.display = 'block';
        }
    </script>
</body>
</html>
    """
    return html_content

def main():
    # Create HTML file
    html_content = generate_html()
    with open('/workspace/quiz-app/quiz.html', 'w') as f:
        f.write(html_content)
    
    print("Quiz application created successfully!")
    print("To run the quiz:")
    print("1. Open quiz.html in your web browser")
    print("2. Or run: python web_quiz.py to start a local server")
    
    # Start a simple HTTP server
    try:
        os.chdir('/workspace/quiz-app')
        httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
        print("\nStarting web server at http://localhost:8000")
        print("Opening quiz in browser...")
        
        # Open browser in a separate thread
        def open_browser():
            time.sleep(1)
            webbrowser.open('http://localhost:8000/quiz.html')
        
        threading.Thread(target=open_browser).start()
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Could not start server: {e}")
        print("You can still open quiz.html directly in your browser.")

if __name__ == "__main__":
    main()
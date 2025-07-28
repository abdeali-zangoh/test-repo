# Quiz Application

A modern, interactive quiz application built with Python that features both desktop (tkinter) and web-based interfaces.

## Features

- **Interactive UI**: Clean, modern interface with smooth animations
- **Multiple Choice Questions**: 8 sample questions covering various topics
- **Progress Tracking**: Visual progress bar and question counter
- **Score Calculation**: Real-time scoring with percentage calculation
- **Randomized Questions**: Questions are shuffled for each quiz session
- **Immediate Feedback**: Shows correct answers after each question
- **Performance Evaluation**: Personalized messages based on score

## Files

- `quiz.py` - Desktop version using tkinter (requires tkinter installation)
- `web_quiz.py` - Web server version that creates and serves an HTML quiz
- `quiz.html` - Standalone HTML/CSS/JavaScript quiz (auto-generated)

## How to Run

### Web Version (Recommended)
```bash
cd quiz-app
python web_quiz.py
```
This will start a local web server at http://localhost:8000 and automatically open the quiz in your browser.

### Desktop Version
```bash
cd quiz-app
python quiz.py
```
Note: Requires tkinter to be installed (`python3-tk` package on Ubuntu/Debian).

### Standalone HTML
You can also open `quiz.html` directly in any modern web browser.

## Quiz Content

The quiz includes 8 questions covering:
- Geography (capitals, oceans)
- Astronomy (planets)
- Mathematics (basic arithmetic)
- Art (famous paintings)
- Programming (languages)
- History (World War II)
- Chemistry (chemical symbols)

## Technical Details

- **Languages**: Python 3.x, HTML5, CSS3, JavaScript
- **GUI Framework**: tkinter (desktop version)
- **Styling**: Modern CSS with gradients and animations
- **Responsive Design**: Works on desktop and mobile browsers
- **No External Dependencies**: Pure Python and vanilla JavaScript
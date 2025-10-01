#!/usr/bin/env python3
"""Tests for Quiz Application"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
import sys

# Mock tkinter before importing the module
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()

from src.quiz_app.quiz import QuizApp


class TestQuizApp:
    """Test cases for QuizApp class"""

    @pytest.fixture
    def root(self):
        """Create a mock Tk root window"""
        mock_root = Mock()
        return mock_root

    @pytest.fixture
    def app(self, root):
        """Create a QuizApp instance with mocked Tk"""
        with patch('src.quiz_app.quiz.tk.Label'), \
             patch('src.quiz_app.quiz.tk.Frame'), \
             patch('src.quiz_app.quiz.tk.Button'), \
             patch('src.quiz_app.quiz.tk.Radiobutton'), \
             patch('src.quiz_app.quiz.ttk.Progressbar'), \
             patch('src.quiz_app.quiz.tk.IntVar'):
            app = QuizApp(root)
            return app

    def test_init(self, root):
        """Test QuizApp initialization"""
        with patch('src.quiz_app.quiz.tk.Label'), \
             patch('src.quiz_app.quiz.tk.Frame'), \
             patch('src.quiz_app.quiz.tk.Button'), \
             patch('src.quiz_app.quiz.tk.Radiobutton'), \
             patch('src.quiz_app.quiz.ttk.Progressbar'), \
             patch('src.quiz_app.quiz.tk.IntVar'):
            app = QuizApp(root)

            assert app.root == root
            assert app.current_question == 0
            assert app.score == 0
            assert app.quiz_started is False
            root.title.assert_called_once_with("Quiz Application")
            root.geometry.assert_called_once_with("800x600")

    def test_load_questions(self, app):
        """Test that questions are loaded correctly"""
        questions = app.load_questions()

        assert len(questions) == 8
        assert questions[0]["question"] == "What is the capital of France?"
        assert questions[0]["options"] == ["London", "Berlin", "Paris", "Madrid"]
        assert questions[0]["correct"] == 2

    def test_load_questions_structure(self, app):
        """Test that all questions have required fields"""
        questions = app.load_questions()

        for question in questions:
            assert "question" in question
            assert "options" in question
            assert "correct" in question
            assert len(question["options"]) == 4
            assert 0 <= question["correct"] <= 3

    def test_start_quiz(self, app):
        """Test starting the quiz"""
        app.welcome_frame = Mock()
        app.quiz_frame = Mock()
        app.progress = {'maximum': 0}

        with patch.object(app, 'display_question') as mock_display:
            app.start_quiz()

            assert app.current_question == 0
            assert app.score == 0
            assert app.quiz_started is True
            app.welcome_frame.pack_forget.assert_called_once()
            app.quiz_frame.pack.assert_called_once()
            mock_display.assert_called_once()

    def test_start_quiz_shuffles_questions(self, app):
        """Test that questions are shuffled when starting quiz"""
        app.welcome_frame = Mock()
        app.quiz_frame = Mock()
        app.progress = {'maximum': 0}

        original_questions = app.questions.copy()

        with patch.object(app, 'display_question'), \
             patch('src.quiz_app.quiz.random.shuffle') as mock_shuffle:
            app.start_quiz()
            mock_shuffle.assert_called_once()

    def test_display_question_first_question(self, app):
        """Test displaying the first question"""
        app.current_question = 0
        app.progress = {'value': 0, 'maximum': 8}
        app.counter_label = Mock()
        app.question_label = Mock()
        app.option_buttons = [Mock() for _ in range(4)]
        app.selected_option = Mock()
        app.submit_btn = Mock()
        app.next_btn = Mock()
        app.score_label = Mock()

        app.display_question()

        app.question_label.config.assert_called_once()
        app.counter_label.config.assert_called_once()
        for btn in app.option_buttons:
            btn.config.assert_called_once()

    def test_display_question_updates_progress(self, app):
        """Test that display_question updates progress correctly"""
        app.current_question = 2
        app.progress = {'value': 0, 'maximum': 8}
        app.counter_label = Mock()
        app.question_label = Mock()
        app.option_buttons = [Mock() for _ in range(4)]
        app.selected_option = Mock()
        app.submit_btn = Mock()
        app.next_btn = Mock()
        app.score_label = Mock()

        app.display_question()

        assert app.progress['value'] == 3

    def test_display_question_last_question(self, app):
        """Test behavior when reaching the last question"""
        app.current_question = len(app.questions)
        app.progress = {'value': 0}
        app.counter_label = Mock()

        with patch.object(app, 'show_results') as mock_show:
            app.display_question()
            mock_show.assert_called_once()

    def test_submit_answer_no_selection(self, app):
        """Test submitting answer without selecting an option"""
        app.selected_option = Mock()
        app.selected_option.get.return_value = -1

        with patch('src.quiz_app.quiz.messagebox.showwarning') as mock_warning:
            app.submit_answer()
            mock_warning.assert_called_once_with("Warning", "Please select an answer!")

    def test_submit_answer_correct(self, app):
        """Test submitting correct answer"""
        app.current_question = 0
        app.score = 0
        app.selected_option = Mock()
        app.selected_option.get.return_value = 2  # Correct answer for first question
        app.submit_btn = Mock()
        app.next_btn = Mock()

        with patch('src.quiz_app.quiz.messagebox.showinfo') as mock_info:
            app.submit_answer()

            assert app.score == 1
            mock_info.assert_called_once_with("Correct!", "Great job! That's the right answer.")
            app.submit_btn.config.assert_called_once_with(state="disabled")

    def test_submit_answer_incorrect(self, app):
        """Test submitting incorrect answer"""
        app.current_question = 0
        app.score = 0
        app.selected_option = Mock()
        app.selected_option.get.return_value = 0  # Incorrect answer
        app.submit_btn = Mock()
        app.next_btn = Mock()

        with patch('src.quiz_app.quiz.messagebox.showinfo') as mock_info:
            app.submit_answer()

            assert app.score == 0
            mock_info.assert_called_once()
            args = mock_info.call_args[0]
            assert args[0] == "Incorrect"
            assert "correct answer was:" in args[1]

    def test_submit_answer_last_question(self, app):
        """Test submitting answer on last question"""
        app.current_question = len(app.questions) - 1
        app.score = 0
        app.selected_option = Mock()
        app.selected_option.get.return_value = app.questions[-1]["correct"]
        app.submit_btn = Mock()
        app.next_btn = Mock()

        with patch('src.quiz_app.quiz.messagebox.showinfo'):
            app.submit_answer()

            app.next_btn.config.assert_called_once_with(text="Show Results", state="normal")

    def test_next_question_advances(self, app):
        """Test that next_question advances to next question"""
        app.current_question = 0

        with patch.object(app, 'display_question') as mock_display:
            app.next_question()

            assert app.current_question == 1
            mock_display.assert_called_once()

    def test_next_question_shows_results_at_end(self, app):
        """Test that next_question shows results when finished"""
        app.current_question = len(app.questions) - 1

        with patch.object(app, 'show_results') as mock_show:
            app.next_question()
            mock_show.assert_called_once()

    def test_show_results_excellent_score(self, app):
        """Test show_results with excellent score (>= 80%)"""
        app.score = 7
        app.quiz_frame = Mock()
        app.main_frame = Mock()

        with patch('src.quiz_app.quiz.tk.Frame') as mock_frame, \
             patch('src.quiz_app.quiz.tk.Label'), \
             patch('src.quiz_app.quiz.tk.Button'):
            app.show_results()
            app.quiz_frame.pack_forget.assert_called_once()

    def test_show_results_good_score(self, app):
        """Test show_results with good score (60-79%)"""
        app.score = 5
        app.quiz_frame = Mock()
        app.main_frame = Mock()

        with patch('src.quiz_app.quiz.tk.Frame') as mock_frame, \
             patch('src.quiz_app.quiz.tk.Label'), \
             patch('src.quiz_app.quiz.tk.Button'):
            app.show_results()
            app.quiz_frame.pack_forget.assert_called_once()

    def test_show_results_average_score(self, app):
        """Test show_results with average score (40-59%)"""
        app.score = 4
        app.quiz_frame = Mock()
        app.main_frame = Mock()

        with patch('src.quiz_app.quiz.tk.Frame') as mock_frame, \
             patch('src.quiz_app.quiz.tk.Label'), \
             patch('src.quiz_app.quiz.tk.Button'):
            app.show_results()
            app.quiz_frame.pack_forget.assert_called_once()

    def test_show_results_low_score(self, app):
        """Test show_results with low score (< 40%)"""
        app.score = 2
        app.quiz_frame = Mock()
        app.main_frame = Mock()

        with patch('src.quiz_app.quiz.tk.Frame') as mock_frame, \
             patch('src.quiz_app.quiz.tk.Label'), \
             patch('src.quiz_app.quiz.tk.Button'):
            app.show_results()
            app.quiz_frame.pack_forget.assert_called_once()

    def test_restart_quiz(self, app):
        """Test restarting the quiz"""
        app.current_question = 5
        app.score = 3
        app.quiz_started = True
        app.main_frame = Mock()
        mock_children = [Mock(), Mock()]
        app.main_frame.winfo_children.return_value = mock_children

        with patch.object(app, 'setup_ui') as mock_setup:
            app.restart_quiz()

            assert app.current_question == 0
            assert app.score == 0
            assert app.quiz_started is False
            mock_setup.assert_called_once()
            for child in mock_children:
                child.destroy.assert_called_once()

    def test_setup_ui_creates_widgets(self, root):
        """Test that setup_ui creates all necessary widgets"""
        with patch('src.quiz_app.quiz.tk.Label') as mock_label, \
             patch('src.quiz_app.quiz.tk.Frame') as mock_frame, \
             patch('src.quiz_app.quiz.tk.Button') as mock_button, \
             patch('src.quiz_app.quiz.tk.Radiobutton') as mock_radio, \
             patch('src.quiz_app.quiz.ttk.Progressbar') as mock_progress, \
             patch('src.quiz_app.quiz.tk.IntVar') as mock_intvar:

            app = QuizApp(root)

            # Verify widgets were created
            assert mock_label.called
            assert mock_frame.called
            assert mock_button.called
            assert mock_radio.called
            assert mock_progress.called
            assert mock_intvar.called

    def test_questions_content_accuracy(self, app):
        """Test specific question content for accuracy"""
        questions = app.questions

        # Test first question
        assert "France" in questions[0]["question"]
        assert "Paris" in questions[0]["options"]

        # Test Mars question
        mars_q = next(q for q in questions if "Mars" in q["question"])
        assert "Mars" in mars_q["options"]

        # Test math question
        math_q = next(q for q in questions if "2 + 2" in q["question"])
        assert "4" in math_q["options"]

    def test_submit_answer_enables_next_button(self, app):
        """Test that submit_answer enables next button for non-last questions"""
        app.current_question = 0
        app.selected_option = Mock()
        app.selected_option.get.return_value = 2
        app.submit_btn = Mock()
        app.next_btn = Mock()

        with patch('src.quiz_app.quiz.messagebox.showinfo'):
            app.submit_answer()
            app.next_btn.config.assert_called_once_with(state="normal")

    def test_display_question_resets_selection(self, app):
        """Test that display_question resets the selected option"""
        app.current_question = 0
        app.progress = {'value': 0, 'maximum': 8}
        app.counter_label = Mock()
        app.question_label = Mock()
        app.option_buttons = [Mock() for _ in range(4)]
        app.selected_option = Mock()
        app.submit_btn = Mock()
        app.next_btn = Mock()
        app.score_label = Mock()

        app.display_question()

        app.selected_option.set.assert_called_once_with(-1)
        app.submit_btn.config.assert_called_once_with(state="normal")
        app.next_btn.config.assert_called_once_with(state="disabled")

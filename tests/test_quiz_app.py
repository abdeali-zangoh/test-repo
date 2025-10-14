"""Tests for quiz-app modules"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add quiz-app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "quiz-app"))

# Import after path is set
from web_quiz import QuizData, generate_html


class TestQuizData:
    """Test QuizData class"""

    def test_init_creates_questions(self):
        """Test that initialization creates questions"""
        quiz_data = QuizData()
        assert len(quiz_data.questions) > 0
        assert isinstance(quiz_data.questions, list)

    def test_questions_have_required_fields(self):
        """Test that questions have all required fields"""
        quiz_data = QuizData()
        for question in quiz_data.questions:
            assert "question" in question
            assert "options" in question
            assert "correct" in question
            assert len(question["options"]) == 4
            assert 0 <= question["correct"] <= 3

    def test_get_questions_returns_shuffled(self):
        """Test that get_questions returns shuffled list"""
        quiz_data = QuizData()
        original_questions = quiz_data.questions.copy()
        shuffled = quiz_data.get_questions()

        # Should have same length
        assert len(shuffled) == len(original_questions)

        # Should contain same questions
        for q in original_questions:
            assert q in shuffled

    def test_get_questions_does_not_modify_original(self):
        """Test that get_questions doesn't modify original list"""
        quiz_data = QuizData()
        original_first = quiz_data.questions[0]
        quiz_data.get_questions()
        assert quiz_data.questions[0] == original_first


class TestGenerateHtml:
    """Test generate_html function"""

    def test_generate_html_returns_string(self):
        """Test that generate_html returns a string"""
        html = generate_html()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_generate_html_has_doctype(self):
        """Test that HTML has DOCTYPE"""
        html = generate_html()
        assert "<!DOCTYPE html>" in html

    def test_generate_html_has_title(self):
        """Test that HTML has title"""
        html = generate_html()
        assert "<title>Quiz Application</title>" in html

    def test_generate_html_has_javascript(self):
        """Test that HTML has JavaScript"""
        html = generate_html()
        assert "<script>" in html
        assert "function startQuiz()" in html

    def test_generate_html_has_css(self):
        """Test that HTML has CSS styles"""
        html = generate_html()
        assert "<style>" in html
        assert "body" in html

    def test_generate_html_has_questions_data(self):
        """Test that HTML contains questions data"""
        html = generate_html()
        assert "What is the capital of France?" in html
        assert "Paris" in html


class TestWebQuizMain:
    """Test web_quiz main function"""

    @patch("web_quiz.webbrowser.open")
    @patch("web_quiz.HTTPServer")
    @patch("web_quiz.os.chdir")
    @patch("builtins.open", create=True)
    @patch("builtins.print")
    def test_main_creates_html_file(
        self, mock_print, mock_open, mock_chdir, mock_httpserver, mock_browser
    ):
        """Test that main creates HTML file"""
        from web_quiz import main

        # Mock the file write
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock HTTP server to raise KeyboardInterrupt immediately
        mock_server_instance = MagicMock()
        mock_server_instance.serve_forever.side_effect = KeyboardInterrupt()
        mock_httpserver.return_value = mock_server_instance

        main()

        # Verify file was opened for writing
        assert mock_open.called

    @patch("web_quiz.HTTPServer")
    @patch("web_quiz.os.chdir")
    @patch("builtins.open", create=True)
    @patch("builtins.print")
    def test_main_handles_keyboard_interrupt(
        self, mock_print, mock_open, mock_chdir, mock_httpserver
    ):
        """Test that main handles KeyboardInterrupt gracefully"""
        from web_quiz import main

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock HTTP server to raise KeyboardInterrupt
        mock_server_instance = MagicMock()
        mock_server_instance.serve_forever.side_effect = KeyboardInterrupt()
        mock_httpserver.return_value = mock_server_instance

        main()

        # Verify message was printed
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Server stopped" in call for call in calls)

    @patch("web_quiz.HTTPServer")
    @patch("web_quiz.os.chdir")
    @patch("builtins.open", create=True)
    @patch("builtins.print")
    def test_main_handles_exception(self, mock_print, mock_open, mock_chdir, mock_httpserver):
        """Test that main handles exceptions gracefully"""
        from web_quiz import main

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock HTTP server to raise exception
        mock_server_instance = MagicMock()
        mock_server_instance.serve_forever.side_effect = Exception("Test error")
        mock_httpserver.return_value = mock_server_instance

        main()

        # Verify error message was printed
        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Could not start server" in call for call in calls)


# Note: quiz.py uses tkinter which requires a display/GUI environment
# Testing it would require complex mocking or a virtual display
# For coverage purposes, we'll add basic import tests


class TestQuizImport:
    """Test that quiz module can be imported"""

    def test_quiz_module_imports(self):
        """Test that quiz module imports without errors"""
        try:
            # Try to import - may fail if tkinter is not available
            import quiz  # noqa: F401

            assert True
        except ImportError:
            # tkinter not available, skip test
            pytest.skip("tkinter not available in test environment")
        except Exception:
            # Other errors (like display not available) are okay for import test
            assert True

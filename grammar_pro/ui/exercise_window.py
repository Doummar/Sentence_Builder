"""
Exercise Window for Grammar Pro.

Window for displaying and interacting with exercises.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget,
    QSizePolicy,
    QMessageBox,
)

if TYPE_CHECKING:
    from ..core.addon_manager import AddonManager
    from ..exercises.base_exercise import BaseExercise, ExerciseResult


class ExerciseWindow(QMainWindow):
    """
    Exercise Window for Grammar Pro.
    
    Displays exercises and handles user interaction.
    """
    
    # Signals
    exercise_completed = pyqtSignal()
    exercise_skipped = pyqtSignal()
    hint_requested = pyqtSignal(int)
    
    def __init__(
        self,
        addon_manager: 'AddonManager',
        mode: str,
        language: str,
        parent: QWidget = None
    ):
        """
        Initialize the exercise window.
        
        Args:
            addon_manager: Addon manager instance
            mode: Exercise mode ID
            language: Language code
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.addon_manager = addon_manager
        self.settings = addon_manager.settings
        self.mode = mode
        self.language = language
        
        # Exercise state
        self.current_exercise: Optional['BaseExercise'] = None
        self.exercise_index = 0
        self.total_exercises = 20  # Default session size
        
        # Window setup
        self.setWindowTitle(f"Grammar Pro - {mode.replace('_', ' ').title()}")
        self.setMinimumSize(QSize(600, 400))
        
        # Apply settings
        self._apply_settings()
        
        # Create UI
        self._create_widgets()
        self._create_layout()
        self._connect_signals()
        
        # Start the first exercise
        self._start_exercise_session()
    
    def _apply_settings(self) -> None:
        """Apply settings to the window."""
        if self.settings:
            # Apply theme
            if self.settings.ui.theme == "dark":
                self._apply_dark_theme()
            elif self.settings.ui.theme == "light":
                self._apply_light_theme()
            
            # Apply font
            if self.settings.ui.font_family:
                font = QFont(self.settings.ui.font_family, self.settings.ui.font_size)
                self.setFont(font)
    
    def _apply_dark_theme(self) -> None:
        """Apply dark theme stylesheet."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
            }
            QPushButton:pressed {
                background-color: #2c2c2c;
            }
            QFrame {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 4px;
            }
        """)
    
    def _apply_light_theme(self) -> None:
        """Apply light theme stylesheet."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                color: #333;
            }
            QWidget {
                background-color: #f0f0f0;
                color: #333;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #ccc;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QFrame {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
    
    def _create_widgets(self) -> None:
        """Create all widgets."""
        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)
        
        # Header
        self.header_frame = QFrame()
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(10, 10, 10, 10)
        self.header_layout.setSpacing(15)
        
        # Progress info
        self.progress_label = QLabel("Exercise 1 of 20")
        self.progress_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Timer
        self.timer_label = QLabel("Time: 00:00")
        self.timer_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Add to header
        self.header_layout.addWidget(self.progress_label)
        self.header_layout.addWidget(self.timer_label)
        self.header_layout.addWidget(self.close_button)
        
        # Exercise display
        self.exercise_frame = QFrame()
        self.exercise_layout = QVBoxLayout(self.exercise_frame)
        self.exercise_layout.setContentsMargins(15, 15, 15, 15)
        self.exercise_layout.setSpacing(15)
        
        # Question/Instruction
        self.question_label = QLabel("Loading exercise...")
        self.question_label.setWordWrap(True)
        question_font = QFont()
        question_font.setPointSize(14)
        question_font.setBold(True)
        self.question_label.setFont(question_font)
        
        # Exercise content (will be populated based on exercise type)
        self.exercise_content = QStackedWidget()
        
        # Feedback area
        self.feedback_frame = QFrame()
        self.feedback_layout = QVBoxLayout(self.feedback_frame)
        self.feedback_layout.setContentsMargins(10, 10, 10, 10)
        self.feedback_layout.setSpacing(10)
        
        self.feedback_label = QLabel("")
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.feedback_layout.addWidget(self.feedback_label)
        
        # Action buttons
        self.actions_frame = QFrame()
        self.actions_layout = QHBoxLayout(self.actions_frame)
        self.actions_layout.setContentsMargins(10, 10, 10, 10)
        self.actions_layout.setSpacing(15)
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        self.hint_button = QPushButton("Hint")
        self.hint_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.skip_button = QPushButton("Skip")
        self.skip_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.next_button = QPushButton("Next")
        self.next_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.next_button.hide()  # Initially hidden
        
        # Add to actions
        self.actions_layout.addWidget(self.submit_button)
        self.actions_layout.addWidget(self.hint_button)
        self.actions_layout.addWidget(self.skip_button)
        self.actions_layout.addWidget(self.next_button)
        
        # Add to exercise layout
        self.exercise_layout.addWidget(self.question_label)
        self.exercise_layout.addWidget(self.exercise_content, 1)
        self.exercise_layout.addWidget(self.feedback_frame)
        self.exercise_layout.addWidget(self.actions_frame)
        
        # Add to main layout
        self.main_layout.addWidget(self.header_frame)
        self.main_layout.addWidget(self.exercise_frame, 1)
        
        # Timer
        self.exercise_timer = QTimer(self)
        self.exercise_timer.timeout.connect(self._update_timer)
        self.exercise_start_time = None
        self.total_exercise_time = 0
    
    def _create_layout(self) -> None:
        """Create the layout."""
        pass  # Layout is created in _create_widgets
    
    def _connect_signals(self) -> None:
        """Connect signals and slots."""
        self.close_button.clicked.connect(self.close)
        self.submit_button.clicked.connect(self._submit_answer)
        self.hint_button.clicked.connect(self._show_hint)
        self.skip_button.clicked.connect(self._skip_exercise)
        self.next_button.clicked.connect(self._next_exercise)
    
    def _start_exercise_session(self) -> None:
        """Start a new exercise session."""
        # Get exercises for the session
        exercises = self.addon_manager.exercise_manager.create_session(
            num_exercises=self.total_exercises,
            mode=self.mode,
            language=self.language
        )
        
        if not exercises:
            QMessageBox.warning(self, "Error", "Could not create exercises. Please try again.")
            self.close()
            return
        
        # Start with the first exercise
        self._load_exercise(exercises[0])
        self.exercise_index = 0
        
        # Start timer
        self.exercise_start_time = datetime.now()
        self.exercise_timer.start(1000)  # Update every second
    
    def _load_exercise(self, exercise: 'BaseExercise') -> None:
        """Load an exercise into the window."""
        self.current_exercise = exercise
        
        # Update progress
        self.progress_label.setText(f"Exercise {self.exercise_index + 1} of {self.total_exercises}")
        
        # Clear previous content
        while self.exercise_content.count():
            widget = self.exercise_content.widget(0)
            self.exercise_content.removeWidget(widget)
            widget.deleteLater()
        
        # Create the appropriate widget for this exercise type
        self._create_exercise_widget(exercise)
        
        # Set question
        if exercise.current_step:
            self.question_label.setText(exercise.current_step.question)
        else:
            self.question_label.setText(exercise.description)
        
        # Clear feedback
        self.feedback_label.setText("")
        self.feedback_label.setStyleSheet("")
        
        # Hide next button, show submit button
        self.next_button.hide()
        self.submit_button.show()
        
        # Start the exercise
        exercise.start()
    
    def _create_exercise_widget(self, exercise: 'BaseExercise') -> None:
        """Create the appropriate widget for the exercise type."""
        from .widgets.sentence_builder_widget import SentenceBuilderWidget
        from .widgets.grammar_decision_widget import GrammarDecisionWidget
        from .widgets.find_mistake_widget import FindMistakeWidget
        from .widgets.missing_word_widget import MissingWordWidget
        
        exercise_type = exercise.exercise_type.value
        
        if exercise_type == "sentence_builder":
            widget = SentenceBuilderWidget(exercise, self)
            widget.answer_submitted.connect(self._on_answer_submitted)
            self.exercise_content.addWidget(widget)
        elif exercise_type == "grammar_decision":
            widget = GrammarDecisionWidget(exercise, self)
            widget.answer_submitted.connect(self._on_answer_submitted)
            self.exercise_content.addWidget(widget)
        elif exercise_type == "find_mistake":
            widget = FindMistakeWidget(exercise, self)
            widget.answer_submitted.connect(self._on_answer_submitted)
            self.exercise_content.addWidget(widget)
        elif exercise_type == "missing_word":
            widget = MissingWordWidget(exercise, self)
            widget.answer_submitted.connect(self._on_answer_submitted)
            self.exercise_content.addWidget(widget)
        else:
            # Generic widget for other exercise types
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.addWidget(QLabel(f"Exercise type: {exercise_type}"))
            layout.addWidget(QLabel("Widget not yet implemented for this exercise type."))
            self.exercise_content.addWidget(widget)
    
    def _on_answer_submitted(self, answer: Any) -> None:
        """Handle answer submission from a widget."""
        if self.current_exercise:
            # Submit the answer
            result = self.current_exercise.submit_answer(answer)
            
            # Show feedback
            self._show_feedback(result)
            
            # If correct and not last step, move to next step
            if result.is_correct and not self.current_exercise.is_last_step:
                self.current_exercise.next_step()
                if self.current_exercise.current_step:
                    self.question_label.setText(self.current_exercise.current_step.question)
                    # Update the widget with the new step
                    self._update_exercise_widget()
            elif result.is_correct and self.current_exercise.is_last_step:
                # Exercise completed correctly
                self._show_next_button()
            else:
                # Incorrect answer, show hint button
                self._show_hint_button()
    
    def _show_feedback(self, result: 'ExerciseResult') -> None:
        """Show feedback for an answer."""
        if result.is_correct:
            self.feedback_label.setText("✓ Correct!")
            self.feedback_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        else:
            self.feedback_label.setText(f"✗ Incorrect. {result.mistakes[0] if result.mistakes else ''}")
            self.feedback_label.setStyleSheet("color: #F44336; font-weight: bold;")
        
        # Show explanation
        if self.current_exercise:
            explanation = self.current_exercise.get_explanation()
            if explanation:
                self.feedback_label.setText(self.feedback_label.text() + f"\n\n{explanation}")
    
    def _show_next_button(self) -> None:
        """Show the next button and hide submit."""
        self.submit_button.hide()
        self.next_button.show()
    
    def _show_hint_button(self) -> None:
        """Show the hint button."""
        self.hint_button.show()
    
    def _update_exercise_widget(self) -> None:
        """Update the exercise widget with the current step."""
        # This would update the widget to show the current step
        # For now, we'll just update the question
        if self.current_exercise and self.current_exercise.current_step:
            self.question_label.setText(self.current_exercise.current_step.question)
    
    def _submit_answer(self) -> None:
        """Handle submit button click."""
        # For exercises that don't have a custom widget, we need to get the answer
        # from the current widget
        current_widget = self.exercise_content.currentWidget()
        
        if hasattr(current_widget, 'get_answer'):
            answer = current_widget.get_answer()
            if self.current_exercise:
                result = self.current_exercise.submit_answer(answer)
                self._show_feedback(result)
                
                if result.is_correct and self.current_exercise.is_last_step:
                    self._show_next_button()
                elif result.is_correct:
                    self.current_exercise.next_step()
                    self._update_exercise_widget()
                else:
                    self._show_hint_button()
    
    def _show_hint(self) -> None:
        """Show a hint for the current exercise."""
        if self.current_exercise:
            hint = self.current_exercise.get_hint(1)  # Get first level hint
            if hint:
                QMessageBox.information(self, "Hint", hint.content)
    
    def _skip_exercise(self) -> None:
        """Skip the current exercise."""
        if self.current_exercise:
            # Record as skipped
            self.exercise_skipped.emit()
        
        self._next_exercise()
    
    def _next_exercise(self) -> None:
        """Move to the next exercise."""
        if self.current_exercise:
            # Record the exercise result
            self.addon_manager.statistics_manager.record_exercise(self.current_exercise)
        
        self.exercise_index += 1
        
        if self.exercise_index < self.total_exercises:
            # Load next exercise
            exercises = self.addon_manager.exercise_manager.create_session(
                num_exercises=self.total_exercises,
                mode=self.mode,
                language=self.language
            )
            if self.exercise_index < len(exercises):
                self._load_exercise(exercises[self.exercise_index])
        else:
            # Session completed
            self._show_session_complete()
    
    def _show_session_complete(self) -> None:
        """Show session complete message."""
        # Stop timer
        self.exercise_timer.stop()
        
        # Show summary
        summary = self.addon_manager.get_statistics_summary()
        
        total = summary.get('total_exercises', 0)
        accuracy = summary.get('accuracy', 0.0)
        
        msg = f"""
        <h2>Session Complete!</h2>
        <p>You completed {self.exercise_index} exercises.</p>
        <p>Overall accuracy: {accuracy:.1%}</p>
        <p>Great job! Keep practicing to improve your grammar skills.</p>
        """
        
        QMessageBox.information(self, "Session Complete", msg)
        
        # Close the window
        self.close()
        
        # Notify that exercise is completed
        self.exercise_completed.emit()
    
    def _update_timer(self) -> None:
        """Update the timer display."""
        if self.exercise_start_time:
            elapsed = (datetime.now() - self.exercise_start_time).total_seconds()
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.timer_label.setText(f"Time: {minutes:02d}:{seconds:02d}")
    
    def closeEvent(self, event: Any) -> None:
        """Handle close event."""
        # Stop timer
        self.exercise_timer.stop()
        
        # Save settings
        if self.settings:
            size = self.size()
            self.settings.ui.window_width = size.width()
            self.settings.ui.window_height = size.height()
            self.settings.save()
        
        super().closeEvent(event)


# Import datetime for timer
from datetime import datetime

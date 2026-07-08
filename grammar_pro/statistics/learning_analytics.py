"""
Learning Analytics for Grammar Pro.

Provides advanced analytics and insights into the user's learning progress.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class GrammarCategoryStats:
    """Statistics for a grammar category."""
    category: str
    total_exercises: int = 0
    correct_count: int = 0
    incorrect_count: int = 0
    accuracy: float = 0.0
    average_response_time: float = 0.0
    last_practiced: Optional[str] = None
    mastery_level: float = 0.0  # 0.0 to 1.0
    
    def update(self, is_correct: bool, response_time: float) -> None:
        """Update statistics with a new exercise result."""
        self.total_exercises += 1
        self.last_practiced = datetime.now().isoformat()
        
        if is_correct:
            self.correct_count += 1
        else:
            self.incorrect_count += 1
        
        # Update accuracy
        if self.total_exercises > 0:
            self.accuracy = self.correct_count / self.total_exercises
        
        # Update average response time
        if self.total_exercises == 1:
            self.average_response_time = response_time
        else:
            self.average_response_time = (
                (self.average_response_time * (self.total_exercises - 1)) + response_time
            ) / self.total_exercises
        
        # Update mastery level (simplified)
        self.mastery_level = self.accuracy
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'category': self.category,
            'total_exercises': self.total_exercises,
            'correct_count': self.correct_count,
            'incorrect_count': self.incorrect_count,
            'accuracy': self.accuracy,
            'average_response_time': self.average_response_time,
            'last_practiced': self.last_practiced,
            'mastery_level': self.mastery_level,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GrammarCategoryStats':
        """Create from dictionary."""
        return cls(
            category=data.get('category', ''),
            total_exercises=data.get('total_exercises', 0),
            correct_count=data.get('correct_count', 0),
            incorrect_count=data.get('incorrect_count', 0),
            accuracy=data.get('accuracy', 0.0),
            average_response_time=data.get('average_response_time', 0.0),
            last_practiced=data.get('last_practiced'),
            mastery_level=data.get('mastery_level', 0.0),
        )


@dataclass
class ExerciseTypeStats:
    """Statistics for an exercise type."""
    exercise_type: str
    total_exercises: int = 0
    correct_count: int = 0
    accuracy: float = 0.0
    average_response_time: float = 0.0
    
    def update(self, is_correct: bool, response_time: float) -> None:
        """Update statistics with a new exercise result."""
        self.total_exercises += 1
        
        if is_correct:
            self.correct_count += 1
        
        if self.total_exercises > 0:
            self.accuracy = self.correct_count / self.total_exercises
        
        if self.total_exercises == 1:
            self.average_response_time = response_time
        else:
            self.average_response_time = (
                (self.average_response_time * (self.total_exercises - 1)) + response_time
            ) / self.total_exercises
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'exercise_type': self.exercise_type,
            'total_exercises': self.total_exercises,
            'correct_count': self.correct_count,
            'accuracy': self.accuracy,
            'average_response_time': self.average_response_time,
        }


@dataclass
class LearningAnalytics:
    """
    Learning Analytics for Grammar Pro.
    
    Tracks and analyzes user learning data to provide insights and recommendations.
    """
    
    # Category statistics
    category_stats: Dict[str, GrammarCategoryStats] = field(default_factory=dict)
    
    # Exercise type statistics
    exercise_type_stats: Dict[str, ExerciseTypeStats] = field(default_factory=dict)
    
    # Overall statistics
    total_exercises: int = 0
    total_correct: int = 0
    total_incorrect: int = 0
    overall_accuracy: float = 0.0
    average_response_time: float = 0.0
    
    # Time-based statistics
    daily_stats: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    weekly_stats: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Streaks
    current_streak: int = 0
    longest_streak: int = 0
    
    # Last activity
    last_activity: Optional[str] = None
    
    def update_with_exercise(self, exercise: Any) -> None:
        """
        Update analytics with a completed exercise.
        
        Args:
            exercise: Completed exercise object
        """
        if not hasattr(exercise, 'results') or not hasattr(exercise, 'grammar_categories'):
            return
        
        # Update overall statistics
        for result in exercise.results:
            self._update_overall(result)
            
            # Update category statistics
            for category in result.grammar_categories:
                self._update_category(category, result)
        
        # Update exercise type statistics
        if hasattr(exercise, 'exercise_type'):
            self._update_exercise_type(exercise.exercise_type.value, exercise.results)
        
        # Update time-based statistics
        if exercise.results:
            timestamp = exercise.results[0].timestamp
            self._update_time_stats(timestamp, exercise.results)
        
        # Update last activity
        self.last_activity = datetime.now().isoformat()
    
    def _update_overall(self, result: Any) -> None:
        """Update overall statistics."""
        self.total_exercises += 1
        
        if result.is_correct:
            self.total_correct += 1
        else:
            self.total_incorrect += 1
        
        if self.total_exercises > 0:
            self.overall_accuracy = self.total_correct / self.total_exercises
        
        # Update average response time
        if self.total_exercises == 1:
            self.average_response_time = result.response_time
        else:
            self.average_response_time = (
                (self.average_response_time * (self.total_exercises - 1)) + result.response_time
            ) / self.total_exercises
    
    def _update_category(self, category: str, result: Any) -> None:
        """Update category statistics."""
        if category not in self.category_stats:
            self.category_stats[category] = GrammarCategoryStats(category=category)
        
        self.category_stats[category].update(result.is_correct, result.response_time)
    
    def _update_exercise_type(self, exercise_type: str, results: List[Any]) -> None:
        """Update exercise type statistics."""
        if exercise_type not in self.exercise_type_stats:
            self.exercise_type_stats[exercise_type] = ExerciseTypeStats(exercise_type=exercise_type)
        
        for result in results:
            self.exercise_type_stats[exercise_type].update(result.is_correct, result.response_time)
    
    def _update_time_stats(self, timestamp: str, results: List[Any]) -> None:
        """Update time-based statistics."""
        try:
            dt = datetime.fromisoformat(timestamp)
            date_str = dt.strftime("%Y-%m-%d")
            week_str = dt.strftime("%Y-W%V")
            
            # Update daily stats
            if date_str not in self.daily_stats:
                self.daily_stats[date_str] = {
                    'total': 0,
                    'correct': 0,
                    'incorrect': 0,
                    'accuracy': 0.0,
                }
            
            for result in results:
                self.daily_stats[date_str]['total'] += 1
                if result.is_correct:
                    self.daily_stats[date_str]['correct'] += 1
                else:
                    self.daily_stats[date_str]['incorrect'] += 1
            
            # Update accuracy
            total = self.daily_stats[date_str]['total']
            if total > 0:
                self.daily_stats[date_str]['accuracy'] = self.daily_stats[date_str]['correct'] / total
            
            # Update weekly stats
            if week_str not in self.weekly_stats:
                self.weekly_stats[week_str] = {
                    'total': 0,
                    'correct': 0,
                    'incorrect': 0,
                    'accuracy': 0.0,
                }
            
            for result in results:
                self.weekly_stats[week_str]['total'] += 1
                if result.is_correct:
                    self.weekly_stats[week_str]['correct'] += 1
                else:
                    self.weekly_stats[week_str]['incorrect'] += 1
            
            # Update accuracy
            total = self.weekly_stats[week_str]['total']
            if total > 0:
                self.weekly_stats[week_str]['accuracy'] = self.weekly_stats[week_str]['correct'] / total
        
        except Exception as e:
            print(f"Error updating time stats: {e}")
    
    def get_weak_areas(self, limit: int = 10, min_exercises: int = 5) -> List[Dict[str, Any]]:
        """
        Get the user's weakest grammar areas.
        
        Args:
            limit: Maximum number of weak areas to return
            min_exercises: Minimum number of exercises to consider a category
            
        Returns:
            List of weak area descriptors
        """
        # Filter categories with enough exercises
        filtered = [
            stats for stats in self.category_stats.values()
            if stats.total_exercises >= min_exercises
        ]
        
        # Sort by accuracy (ascending)
        filtered.sort(key=lambda x: x.accuracy)
        
        # Return top weak areas
        result = []
        for stats in filtered[:limit]:
            result.append({
                'category': stats.category,
                'accuracy': stats.accuracy,
                'total_exercises': stats.total_exercises,
                'correct_count': stats.correct_count,
                'incorrect_count': stats.incorrect_count,
                'mastery_level': stats.mastery_level,
                'last_practiced': stats.last_practiced,
            })
        
        return result
    
    def get_strong_areas(self, limit: int = 10, min_exercises: int = 5) -> List[Dict[str, Any]]:
        """
        Get the user's strongest grammar areas.
        
        Args:
            limit: Maximum number of strong areas to return
            min_exercises: Minimum number of exercises to consider a category
            
        Returns:
            List of strong area descriptors
        """
        # Filter categories with enough exercises
        filtered = [
            stats for stats in self.category_stats.values()
            if stats.total_exercises >= min_exercises
        ]
        
        # Sort by accuracy (descending)
        filtered.sort(key=lambda x: x.accuracy, reverse=True)
        
        # Return top strong areas
        result = []
        for stats in filtered[:limit]:
            result.append({
                'category': stats.category,
                'accuracy': stats.accuracy,
                'total_exercises': stats.total_exercises,
                'correct_count': stats.correct_count,
                'incorrect_count': stats.incorrect_count,
                'mastery_level': stats.mastery_level,
                'last_practiced': stats.last_practiced,
            })
        
        return result
    
    def get_learning_progress(self) -> Dict[str, Any]:
        """
        Get the user's learning progress.
        
        Returns:
            Dictionary with progress information
        """
        # Calculate overall mastery
        if self.category_stats:
            total_mastery = sum(stats.mastery_level for stats in self.category_stats.values())
            avg_mastery = total_mastery / len(self.category_stats)
        else:
            avg_mastery = 0.0
        
        # Calculate completion percentage
        # This would be based on the total number of possible exercises
        # For now, we'll use a simplified calculation
        completion_percentage = min(100, self.total_exercises / 100)  # Assuming 100 exercises = 100%
        
        return {
            'overall_accuracy': self.overall_accuracy,
            'total_exercises': self.total_exercises,
            'total_correct': self.total_correct,
            'total_incorrect': self.total_incorrect,
            'average_response_time': self.average_response_time,
            'average_mastery': avg_mastery,
            'completion_percentage': completion_percentage,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_activity': self.last_activity,
        }
    
    def get_daily_stats(self, days: int = 7) -> Dict[str, Dict[str, Any]]:
        """
        Get daily statistics for the last N days.
        
        Args:
            days: Number of days to include
            
        Returns:
            Dictionary with daily statistics
        """
        # Sort daily stats by date
        sorted_daily = dict(sorted(self.daily_stats.items()))
        
        # Get the last N days
        if len(sorted_daily) <= days:
            return sorted_daily
        
        # Get the last N keys
        last_days = list(sorted_daily.keys())[-days:]
        return {k: sorted_daily[k] for k in last_days}
    
    def get_weekly_stats(self, weeks: int = 4) -> Dict[str, Dict[str, Any]]:
        """
        Get weekly statistics for the last N weeks.
        
        Args:
            weeks: Number of weeks to include
            
        Returns:
            Dictionary with weekly statistics
        """
        # Sort weekly stats by week
        sorted_weekly = dict(sorted(self.weekly_stats.items()))
        
        # Get the last N weeks
        if len(sorted_weekly) <= weeks:
            return sorted_weekly
        
        # Get the last N keys
        last_weeks = list(sorted_weekly.keys())[-weeks:]
        return {k: sorted_weekly[k] for k in last_weeks}
    
    def get_accuracy_trend(self, days: int = 30) -> List[Tuple[str, float]]:
        """
        Get the accuracy trend over time.
        
        Args:
            days: Number of days to include
            
        Returns:
            List of (date, accuracy) tuples
        """
        daily = self.get_daily_stats(days)
        trend = []
        
        for date, stats in daily.items():
            trend.append((date, stats.get('accuracy', 0.0)))
        
        return trend
    
    def get_mastery_by_category(self) -> Dict[str, float]:
        """
        Get mastery level by category.
        
        Returns:
            Dictionary mapping category to mastery level
        """
        return {category: stats.mastery_level for category, stats in self.category_stats.items()}
    
    def get_exercise_distribution(self) -> Dict[str, int]:
        """
        Get the distribution of exercises by type.
        
        Returns:
            Dictionary mapping exercise type to count
        """
        return {ex_type: stats.total_exercises for ex_type, stats in self.exercise_type_stats.items()}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'category_stats': {k: v.to_dict() for k, v in self.category_stats.items()},
            'exercise_type_stats': {k: v.to_dict() for k, v in self.exercise_type_stats.items()},
            'total_exercises': self.total_exercises,
            'total_correct': self.total_correct,
            'total_incorrect': self.total_incorrect,
            'overall_accuracy': self.overall_accuracy,
            'average_response_time': self.average_response_time,
            'daily_stats': self.daily_stats,
            'weekly_stats': self.weekly_stats,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_activity': self.last_activity,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LearningAnalytics':
        """Create from dictionary."""
        analytics = cls()
        
        # Load category stats
        for category, stats_data in data.get('category_stats', {}).items():
            analytics.category_stats[category] = GrammarCategoryStats.from_dict(stats_data)
        
        # Load exercise type stats
        for ex_type, stats_data in data.get('exercise_type_stats', {}).items():
            analytics.exercise_type_stats[ex_type] = ExerciseTypeStats(
                exercise_type=ex_type,
                total_exercises=stats_data.get('total_exercises', 0),
                correct_count=stats_data.get('correct_count', 0),
                accuracy=stats_data.get('accuracy', 0.0),
                average_response_time=stats_data.get('average_response_time', 0.0),
            )
        
        # Load overall stats
        analytics.total_exercises = data.get('total_exercises', 0)
        analytics.total_correct = data.get('total_correct', 0)
        analytics.total_incorrect = data.get('total_incorrect', 0)
        analytics.overall_accuracy = data.get('overall_accuracy', 0.0)
        analytics.average_response_time = data.get('average_response_time', 0.0)
        analytics.daily_stats = data.get('daily_stats', {})
        analytics.weekly_stats = data.get('weekly_stats', {})
        analytics.current_streak = data.get('current_streak', 0)
        analytics.longest_streak = data.get('longest_streak', 0)
        analytics.last_activity = data.get('last_activity')
        
        return analytics

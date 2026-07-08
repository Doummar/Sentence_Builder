"""
Statistics Manager for Grammar Pro.

Manages all statistics collection, storage, and retrieval.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from .learning_analytics import LearningAnalytics

if TYPE_CHECKING:
    from ..config.settings import Settings
    from ..persistence.data_manager import DataManager
    from ..exercises.base_exercise import BaseExercise, ExerciseResult


@dataclass
class StatisticsData:
    """Container for all statistics data."""
    analytics: LearningAnalytics = field(default_factory=LearningAnalytics)
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'analytics': self.analytics.to_dict(),
            'last_updated': self.last_updated,
            'version': self.version,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StatisticsData':
        """Create from dictionary."""
        analytics = LearningAnalytics.from_dict(data.get('analytics', {}))
        return cls(
            analytics=analytics,
            last_updated=data.get('last_updated', datetime.now().isoformat()),
            version=data.get('version', "1.0"),
        )


class StatisticsManager:
    """
    Statistics Manager for Grammar Pro.
    
    Responsibilities:
    - Collect and store exercise results
    - Track learning progress
    - Provide analytics and insights
    - Manage adaptive learning data
    """
    
    def __init__(self, data_manager: 'DataManager', settings: 'Settings' = None):
        """
        Initialize the Statistics Manager.
        
        Args:
            data_manager: Data manager instance
            settings: Settings instance
        """
        self.data_manager = data_manager
        self.settings = settings
        self._analytics = LearningAnalytics()
        self._initialized = False
    
    def initialize(self) -> bool:
        """Initialize the statistics manager."""
        if self._initialized:
            return True
        
        # Load existing statistics
        stats_data = self.data_manager.load_statistics()
        if stats_data:
            try:
                statistics_data = StatisticsData.from_dict(stats_data)
                self._analytics = statistics_data.analytics
            except Exception as e:
                print(f"Error loading statistics: {e}")
        
        self._initialized = True
        return True
    
    def shutdown(self) -> None:
        """Shutdown the statistics manager."""
        # Save statistics before shutdown
        self.save()
        self._initialized = False
    
    def save(self) -> bool:
        """Save statistics to storage."""
        if not self._initialized:
            if not self.initialize():
                return False
        
        statistics_data = StatisticsData(
            analytics=self._analytics,
            last_updated=datetime.now().isoformat(),
        )
        
        return self.data_manager.save_statistics(statistics_data)
    
    def record_exercise(self, exercise: 'BaseExercise') -> None:
        """
        Record a completed exercise.
        
        Args:
            exercise: Completed exercise
        """
        if not self._initialized:
            self.initialize()
        
        # Update analytics
        self._analytics.update_with_exercise(exercise)
        
        # Save to data manager
        self.data_manager.record_exercise_result(exercise)
        
        # Periodically save statistics
        if exercise.results and len(exercise.results) % 10 == 0:
            self.save()
    
    def record_exercise_result(self, result: 'ExerciseResult') -> None:
        """
        Record an individual exercise result.
        
        Args:
            result: Exercise result to record
        """
        if not self._initialized:
            self.initialize()
        
        # This is called for individual results
        # We'll update analytics directly
        self._analytics.update_with_exercise(result)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of user statistics.
        
        Returns:
            Dictionary with statistics summary
        """
        if not self._initialized:
            self.initialize()
        
        return self._analytics.get_learning_progress()
    
    def get_weak_areas(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the user's weakest grammar areas.
        
        Args:
            limit: Maximum number of weak areas to return
            
        Returns:
            List of weak area descriptors
        """
        if not self._initialized:
            self.initialize()
        
        return self._analytics.get_weak_areas(limit)
    
    def get_strong_areas(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the user's strongest grammar areas.
        
        Args:
            limit: Maximum number of strong areas to return
            
        Returns:
            List of strong area descriptors
        """
        if not self._initialized:
            self.initialize()
        
        return self._analytics.get_strong_areas(limit)
    
    def get_learning_progress(self) -> Dict[str, Any]:
        """
        Get the user's learning progress.
        
        Returns:
            Dictionary with progress information
        """
        if not self._initialized:
            self.initialize()
        
        return self._analytics.get_learning_progress()
    
    def get_daily_stats(self, days: int = 7) -> Dict[str, Dict[str, Any]]:
        """
        Get daily statistics.
        
        Args:
            days: Number of days to include
            
        Returns:
            Dictionary with daily statistics
        """
        if not self._initialized:
            self.initialize()
        
        return self._analytics.get_daily_stats(days)
    
    def get_weekly_stats(self, weeks: int = 4) -> Dict[str, Dict[str, Any]]:
        """
        Get weekly statistics.
        
        Args:
            weeks: Number of weeks to include
            
        Returns:
            Dictionary with weekly statistics
        """
        if not self._initialized:
            self.initialize()
        
        return self._analytics.get_weekly_stats(weeks)
    
    def get_accuracy_trend(self, days: int = 30) -> List[Tuple[str, float]]:
        """
        Get the accuracy trend over time.
        
        Args:
            days: Number of days to include
            
        Returns:
            List of (date, accuracy) tuples
        """
        if not self._initialized:
            self.initialize()
        
        return self._analytics.get_accuracy_trend(days)
    
    def get_mastery_by_category(self) -> Dict[str, float]:
        """
        Get mastery level by category.
        
        Returns:
            Dictionary mapping category to mastery level
        """
        if not self._initialized:
            self.initialize()
        
        return self._analytics.get_mastery_by_category()
    
    def get_exercise_distribution(self) -> Dict[str, int]:
        """
        Get the distribution of exercises by type.
        
        Returns:
            Dictionary mapping exercise type to count
        """
        if not self._initialized:
            self.initialize()
        
        return self._analytics.get_exercise_distribution()
    
    def get_category_stats(self, category: str) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a specific category.
        
        Args:
            category: Grammar category
            
        Returns:
            Category statistics, or None if not found
        """
        if not self._initialized:
            self.initialize()
        
        if category in self._analytics.category_stats:
            stats = self._analytics.category_stats[category]
            return {
                'category': stats.category,
                'total_exercises': stats.total_exercises,
                'correct_count': stats.correct_count,
                'incorrect_count': stats.incorrect_count,
                'accuracy': stats.accuracy,
                'average_response_time': stats.average_response_time,
                'mastery_level': stats.mastery_level,
                'last_practiced': stats.last_practiced,
            }
        
        return None
    
    def get_adaptive_recommendations(self, num_recommendations: int = 5) -> List[Dict[str, Any]]:
        """
        Get exercise recommendations based on adaptive learning.
        
        Args:
            num_recommendations: Number of recommendations to return
            
        Returns:
            List of exercise recommendations
        """
        if not self._initialized:
            self.initialize()
        
        # Get weak areas
        weak_areas = self.get_weak_areas()
        
        # Map categories to exercise types
        category_exercises = {
            'word_order': ['sentence_builder', 'inversion'],
            'negation': ['negation', 'find_mistake'],
            'questions': ['grammar_decision', 'transformation'],
            'clauses': ['clause_trainer', 'subordinate_clause'],
            'verbs': ['transformation', 'sentence_builder'],
        }
        
        recommendations = []
        for weak_area in weak_areas:
            category = weak_area['category']
            if category in category_exercises:
                for exercise_type in category_exercises[category]:
                    recommendations.append({
                        'exercise_type': exercise_type,
                        'category': category,
                        'accuracy': weak_area['accuracy'],
                        'total_exercises': weak_area['total_exercises'],
                        'reason': f"Low accuracy ({weak_area['accuracy']:.0%}) in {category}",
                        'priority': 1 - weak_area['accuracy']  # Higher priority for lower accuracy
                    })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return recommendations[:num_recommendations]
    
    def get_mastery_percentage(self) -> float:
        """
        Get the overall mastery percentage.
        
        Returns:
            Mastery percentage (0.0 to 100.0)
        """
        if not self._initialized:
            self.initialize()
        
        progress = self.get_learning_progress()
        return progress.get('completion_percentage', 0.0)
    
    def get_recent_improvement(self, days: int = 7) -> float:
        """
        Get the recent improvement in accuracy.
        
        Args:
            days: Number of days to compare
            
        Returns:
            Improvement percentage (can be negative)
        """
        if not self._initialized:
            self.initialize()
        
        # Get accuracy trend
        trend = self._analytics.get_accuracy_trend(days * 2)
        
        if len(trend) < 2:
            return 0.0
        
        # Compare first and last
        first_accuracy = trend[0][1] if trend else 0.0
        last_accuracy = trend[-1][1] if trend else 0.0
        
        return (last_accuracy - first_accuracy) * 100  # Convert to percentage
    
    def get_common_mistakes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the user's most common mistakes.
        
        Args:
            limit: Maximum number of mistakes to return
            
        Returns:
            List of common mistake descriptors
        """
        if not self._initialized:
            self.initialize()
        
        # This would require tracking individual mistakes
        # For now, return a placeholder
        weak_areas = self.get_weak_areas(limit)
        return [
            {
                'category': area['category'],
                'count': area['incorrect_count'],
                'description': f"Struggles with {area['category']}"
            }
            for area in weak_areas
        ]
    
    def reset_statistics(self) -> None:
        """Reset all statistics."""
        self._analytics = LearningAnalytics()
        self.save()

#!/usr/bin/env python3
"""
Simple test script to verify Grammar Pro addon structure.
"""

import sys
import os

# Add the grammar_pro directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from grammar_pro import init_addon, get_addon_manager
        print("✓ Main module imports successfully")
    except Exception as e:
        print(f"✗ Main module import failed: {e}")
        return False
    
    try:
        from grammar_pro.config.settings import Settings
        from grammar_pro.config.user_preferences import UserPreferences
        print("✓ Config module imports successfully")
    except Exception as e:
        print(f"✗ Config module import failed: {e}")
        return False
    
    try:
        from grammar_pro.core.addon_manager import AddonManager
        from grammar_pro.core.anki_integration import setup_anki_hooks
        print("✓ Core module imports successfully")
    except Exception as e:
        print(f"✗ Core module import failed: {e}")
        return False
    
    try:
        from grammar_pro.grammar.grammar_engine import GrammarEngine
        from grammar_pro.grammar.base_grammar import BaseGrammar, Word, WordType
        from grammar_pro.grammar.danish_grammar import DanishGrammar
        from grammar_pro.grammar.english_grammar import EnglishGrammar
        print("✓ Grammar module imports successfully")
    except Exception as e:
        print(f"✗ Grammar module import failed: {e}")
        return False
    
    try:
        from grammar_pro.exercises.base_exercise import BaseExercise, ExerciseType
        from grammar_pro.exercises.exercise_manager import ExerciseManager
        from grammar_pro.exercises.sentence_builder import SentenceBuilderExercise
        from grammar_pro.exercises.grammar_decision import GrammarDecisionExercise
        from grammar_pro.exercises.find_mistake import FindMistakeExercise
        print("✓ Exercises module imports successfully")
    except Exception as e:
        print(f"✗ Exercises module import failed: {e}")
        return False
    
    try:
        from grammar_pro.persistence.data_manager import DataManager
        from grammar_pro.persistence.storage_backend import StorageBackend, JSONStorageBackend
        print("✓ Persistence module imports successfully")
    except Exception as e:
        print(f"✗ Persistence module import failed: {e}")
        return False
    
    try:
        from grammar_pro.statistics.statistics_manager import StatisticsManager
        from grammar_pro.statistics.learning_analytics import LearningAnalytics
        print("✓ Statistics module imports successfully")
    except Exception as e:
        print(f"✗ Statistics module import failed: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from grammar_pro.config.settings import Settings
        settings = Settings()
        print("✓ Settings created successfully")
    except Exception as e:
        print(f"✗ Settings creation failed: {e}")
        return False
    
    try:
        from grammar_pro.grammar.grammar_engine import GrammarEngine
        engine = GrammarEngine(settings)
        print("✓ GrammarEngine created successfully")
    except Exception as e:
        print(f"✗ GrammarEngine creation failed: {e}")
        return False
    
    try:
        languages = engine.get_available_languages()
        print(f"✓ Available languages: {[lang['name'] for lang in languages]}")
    except Exception as e:
        print(f"✗ Get languages failed: {e}")
        return False
    
    try:
        sentence = engine.generate_sentence(language_code='da')
        print(f"✓ Generated Danish sentence: {' '.join(w.text for w in sentence)}")
    except Exception as e:
        print(f"✗ Generate sentence failed: {e}")
        return False
    
    try:
        from grammar_pro.grammar.danish_grammar import DanishGrammar
        grammar = DanishGrammar()
        rules = grammar.get_rules()
        print(f"✓ Danish grammar has {len(rules)} rules")
    except Exception as e:
        print(f"✗ Danish grammar failed: {e}")
        return False
    
    return True


def test_exercise_creation():
    """Test exercise creation."""
    print("\nTesting exercise creation...")
    
    try:
        from grammar_pro.config.settings import Settings
        from grammar_pro.grammar.grammar_engine import GrammarEngine
        from grammar_pro.exercises.exercise_manager import ExerciseManager
        
        settings = Settings()
        engine = GrammarEngine(settings)
        manager = ExerciseManager(engine, settings)
        
        # Create a sentence builder exercise
        exercise = manager.create_exercise(
            exercise_type=ExerciseType.SENTENCE_BUILDER,
            language='da'
        )
        print(f"✓ Created exercise: {exercise.name}")
        
        # Generate the exercise
        exercise.generate()
        print(f"✓ Exercise generated with {len(exercise.steps)} steps")
        
    except Exception as e:
        print(f"✗ Exercise creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Grammar Pro Addon - Structure Test")
    print("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test basic functionality
    if not test_basic_functionality():
        all_passed = False
    
    # Test exercise creation
    if not test_exercise_creation():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

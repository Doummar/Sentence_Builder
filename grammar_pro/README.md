# Grammar Pro - Anki Addon

A comprehensive Anki addon for learning sentence construction and grammar. Grammar Pro teaches language learners how to **THINK** when building sentences through thousands of small grammar decisions, rather than simply memorizing complete sentences.

## Features

### Educational Philosophy
Grammar Pro is based on proven learning principles:
- **Active Recall**: Retrieve information from memory
- **Retrieval Practice**: Strengthen memory through repeated recall
- **Deliberate Practice**: Focused, targeted practice
- **Immediate Feedback**: Instant correction and explanation
- **Scaffolding**: Gradual support removal as skills improve
- **Error-Based Learning**: Learn from mistakes
- **Progressive Difficulty**: Start simple, gradually increase complexity
- **Spaced Repetition**: Optimized review timing
- **Adaptive Learning**: Personalized practice based on performance
- **Cognitive Load Reduction**: Manageable, focused exercises

### Exercise Modes

1. **Sentence Builder**: Drag words into the correct order
2. **Grammar Decision Trainer**: Answer grammar questions step-by-step
3. **Find the Mistake**: Identify and correct errors in sentences
4. **Missing Word Order**: Fill in missing words in partial sentences
5. **Clause Trainer**: Build main and subordinate clauses separately, then combine
6. **Transformation Trainer**: Convert sentences through various forms (statement → question → negative → past tense → etc.)
7. **Inversion Practice**: Practice V2 word order with hundreds of examples
8. **Negation Trainer**: Practice placement of negation words
9. **Subordinate Clause Trainer**: Practice subordinate clause word order
10. **Mixed Challenge**: Comprehensive exercises combining multiple concepts

### Progressive Learning

14 difficulty levels that gradually introduce grammar concepts:
1. Subject + Verb
2. Subject + Verb + Object
3. Adjectives
4. Adverbs
5. Time expressions
6. Place expressions
7. Negation
8. Questions
9. Modal verbs
10. Fronting
11. V2 rule
12. Subordinate clauses
13. Relative clauses
14. Long sentences

### Adaptive Learning

The addon monitors every answer and tracks:
- Response time
- Mistakes
- Repeated mistakes
- Grammar category performance
- Confidence levels
- Success rate

If you struggle with a concept (e.g., V2 word order), Grammar Pro automatically increases practice for that concept until you master it.

### Error Detection

Every mistake is categorized:
- Wrong verb position
- Wrong subject position
- Wrong adjective order
- Wrong adverb placement
- Wrong negation
- Wrong tense
- Wrong subordinate clause order
- Wrong punctuation
- Wrong agreement
- Wrong article

### Supported Languages

- **Danish** (fully implemented)
- **English** (basic implementation for testing)

The modular architecture makes it easy to add new languages by creating language-specific grammar definitions.

### Statistics Dashboard

Comprehensive analytics including:
- Accuracy by grammar topic
- Response time tracking
- Weakest grammar concepts
- Strongest grammar concepts
- Learning progress over time
- Mastery percentage
- Recent improvement
- Common mistakes

### Custom Exercise Builder

Create your own grammar exercises with:
- Manual entry
- CSV import
- JSON import
- Future: AI generation

## Architecture

Grammar Pro uses a clean, modular architecture:

```
grammar_pro/
├── core/              # Main addon integration
│   ├── addon_manager.py
│   └── anki_integration.py
├── config/            # Configuration
│   ├── settings.py
│   └── user_preferences.py
├── grammar/           # Grammar engine
│   ├── base_grammar.py
│   ├── grammar_engine.py
│   ├── danish_grammar.py
│   └── english_grammar.py
├── exercises/         # Exercise system
│   ├── base_exercise.py
│   ├── exercise_manager.py
│   ├── sentence_builder.py
│   ├── grammar_decision.py
│   ├── find_mistake.py
│   ├── missing_word.py
│   ├── clause_trainer.py
│   ├── transformation.py
│   ├── inversion.py
│   ├── negation.py
│   ├── subordinate_clause.py
│   └── mixed_challenge.py
├── persistence/       # Data storage
│   ├── storage_backend.py
│   └── data_manager.py
├── statistics/        # Learning analytics
│   ├── learning_analytics.py
│   └── statistics_manager.py
├── ui/                # User interface
│   ├── main_window.py
│   ├── exercise_window.py
│   ├── dashboard.py
│   ├── settings_dialog.py
│   ├── exercise_builder.py
│   └── widgets/
│       ├── word_drag_widget.py
│       ├── sentence_builder_widget.py
│       ├── grammar_decision_widget.py
│       ├── find_mistake_widget.py
│       ├── missing_word_widget.py
│       ├── progress_bar.py
│       └── statistics_chart.py
└── tests/             # Automated tests
    ├── test_grammar_engine.py
    ├── test_exercise_manager.py
    └── test_statistics.py
```

## Installation

1. Download the latest release from GitHub
2. In Anki, go to Tools → Add-ons → Get Add-ons
3. Enter the addon code (available from AnkiWeb)
4. Restart Anki

Or manually:
1. Clone this repository
2. Copy the `grammar_pro` folder to your Anki addons directory
3. Restart Anki

## Usage

1. Open Anki
2. Go to Grammar Pro menu
3. Select a language and exercise mode
4. Click "Start Exercise"
5. Complete the exercises and learn!

## Future Features

- More languages (German, French, Spanish, etc.)
- AI-powered exercise generation
- AI-powered mistake explanation
- Personalized grammar lessons
- Advanced adaptive learning algorithms
- Mobile support
- Cloud sync

## Development

### Requirements

- Python 3.9+
- Anki 2.1.45+
- PyQt6

### Running Tests

```bash
python -m unittest discover grammar_pro/tests
```

### Adding a New Language

1. Create a new file in `grammar_pro/grammar/` (e.g., `french_grammar.py`)
2. Inherit from `BaseGrammar`
3. Implement all required methods
4. Register the grammar in `GrammarEngine.__init__()`

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Credits

- **Concept**: Based on language learning research and pedagogy
- **Architecture**: Clean, modular design following SOLID principles
- **Implementation**: Python, PyQt6, Anki Addon API

## Contact

For questions, suggestions, or bug reports, please open an issue on GitHub.

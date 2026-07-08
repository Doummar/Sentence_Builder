"""
English Grammar implementation for Grammar Pro.

Simplified English grammar for testing and comparison.
"""

from typing import Any, Dict, List, Optional, Tuple

from .base_grammar import (
    BaseGrammar,
    GrammarRule,
    SentenceTemplate,
    SentenceType,
    Word,
    WordType,
)


class EnglishGrammar(BaseGrammar):
    """
    English grammar implementation.
    
    Implements basic English grammar rules for testing.
    """
    
    language_code = "en"
    language_name = "English"
    
    def __init__(self, settings=None):
        """Initialize English grammar."""
        self.default_word_order = [
            WordType.SUBJECT,
            WordType.VERB,
            WordType.OBJECT,
            WordType.ADVERB,
            WordType.TIME_EXPRESSION,
            WordType.PLACE_EXPRESSION,
        ]
        
        self.question_word_order = [
            WordType.AUXILIARY,
            WordType.SUBJECT,
            WordType.VERB,
            WordType.OBJECT,
        ]
        
        self.subordinate_clause_order = [
            WordType.SUBJECT,
            WordType.VERB,
            WordType.OBJECT,
        ]
        
        super().__init__(settings)
    
    def _initialize_rules(self) -> None:
        """Initialize English grammar rules."""
        
        # Subject + Verb
        self.rules["en_subject_verb"] = GrammarRule(
            rule_id="en_subject_verb",
            name="Subject + Verb Order",
            description="In English, the subject comes before the verb in statements.",
            category="word_order",
            level=1,
            validation_func=self._validate_subject_verb,
            explanation="English statements follow Subject-Verb-Object order.",
            examples=["I eat", "She runs", "They sleep"],
            counter_examples=["Eat I", "Runs she"]
        )
        
        # SVO Order
        self.rules["en_svo"] = GrammarRule(
            rule_id="en_svo",
            name="Subject-Verb-Object Order",
            description="English uses Subject-Verb-Object order in main clauses.",
            category="word_order",
            level=2,
            validation_func=self._validate_svo,
            explanation="The basic English sentence structure is Subject-Verb-Object.",
            examples=["I eat apples", "She reads books"],
            counter_examples=["I apples eat", "Eat I apples"]
        )
        
        # Questions with auxiliary
        self.rules["en_question_auxiliary"] = GrammarRule(
            rule_id="en_question_auxiliary",
            name="Question with Auxiliary",
            description="Yes/no questions use auxiliary + subject + verb.",
            category="questions",
            level=8,
            validation_func=self._validate_question_auxiliary,
            explanation="English yes/no questions use do/does/did or other auxiliaries before the subject.",
            examples=["Do you eat?", "Does she run?", "Did they sleep?"],
            counter_examples=["You eat?", "She runs?"]
        )
        
        # Negation
        self.rules["en_negation"] = GrammarRule(
            rule_id="en_negation",
            name="Negation with 'not'",
            description="The negation 'not' comes after the auxiliary verb.",
            category="negation",
            level=7,
            validation_func=self._validate_negation,
            explanation="In English, 'not' comes after the auxiliary verb (do/does/did/am/is/are/have/etc.).",
            examples=["I do not eat", "She does not run", "They have not slept"],
            counter_examples=["I not do eat", "Not I eat"]
        )
    
    def _initialize_templates(self) -> None:
        """Initialize English sentence templates."""
        self.templates["en_sv"] = SentenceTemplate(
            template_id="en_sv",
            name="Subject + Verb",
            structure=[WordType.SUBJECT, WordType.VERB],
            required_rules=["en_subject_verb"],
            level=1,
            category="basic",
            examples=["I eat", "She runs"]
        )
        
        self.templates["en_svo"] = SentenceTemplate(
            template_id="en_svo",
            name="Subject + Verb + Object",
            structure=[WordType.SUBJECT, WordType.VERB, WordType.OBJECT],
            required_rules=["en_svo"],
            level=2,
            category="basic",
            examples=["I eat apples", "She reads books"]
        )
        
        self.templates["en_question"] = SentenceTemplate(
            template_id="en_question",
            name="Yes/No Question",
            structure=[WordType.AUXILIARY, WordType.SUBJECT, WordType.VERB, WordType.OBJECT],
            required_rules=["en_question_auxiliary"],
            level=8,
            category="questions",
            examples=["Do you eat?", "Does she run?"]
        )
        
        self.templates["en_negation"] = SentenceTemplate(
            template_id="en_negation",
            name="Negation",
            structure=[WordType.SUBJECT, WordType.AUXILIARY, WordType.NEGATION, WordType.VERB, WordType.OBJECT],
            required_rules=["en_negation"],
            level=7,
            category="negation",
            examples=["I do not eat", "She does not run"]
        )
    
    def _initialize_words(self) -> None:
        """Initialize English word database."""
        # Pronouns
        self.words["i"] = Word(text="I", word_type=WordType.PRONOUN, base_form="I", person=1, number="singular")
        self.words["you"] = Word(text="you", word_type=WordType.PRONOUN, base_form="you", person=2, number="singular")
        self.words["he"] = Word(text="he", word_type=WordType.PRONOUN, base_form="he", person=3, number="singular")
        self.words["she"] = Word(text="she", word_type=WordType.PRONOUN, base_form="she", person=3, number="singular")
        self.words["it"] = Word(text="it", word_type=WordType.PRONOUN, base_form="it", person=3, number="singular")
        self.words["we"] = Word(text="we", word_type=WordType.PRONOUN, base_form="we", person=1, number="plural")
        self.words["they"] = Word(text="they", word_type=WordType.PRONOUN, base_form="they", person=3, number="plural")
        
        # Verbs
        self.words["eat"] = Word(text="eat", word_type=WordType.VERB, base_form="eat", is_finite=False)
        self.words["eats"] = Word(text="eats", word_type=WordType.VERB, base_form="eat", is_finite=True, past_tense="ate")
        self.words["run"] = Word(text="run", word_type=WordType.VERB, base_form="run", is_finite=False)
        self.words["runs"] = Word(text="runs", word_type=WordType.VERB, base_form="run", is_finite=True, past_tense="ran")
        self.words["sleep"] = Word(text="sleep", word_type=WordType.VERB, base_form="sleep", is_finite=False)
        self.words["sleeps"] = Word(text="sleeps", word_type=WordType.VERB, base_form="sleep", is_finite=True, past_tense="slept")
        self.words["read"] = Word(text="read", word_type=WordType.VERB, base_form="read", is_finite=False)
        self.words["reads"] = Word(text="reads", word_type=WordType.VERB, base_form="read", is_finite=True, past_tense="read")
        
        # Auxiliaries
        self.words["do"] = Word(text="do", word_type=WordType.AUXILIARY, is_auxiliary=True, is_finite=True)
        self.words["does"] = Word(text="does", word_type=WordType.AUXILIARY, is_auxiliary=True, is_finite=True)
        self.words["did"] = Word(text="did", word_type=WordType.AUXILIARY, is_auxiliary=True, is_finite=True)
        self.words["am"] = Word(text="am", word_type=WordType.AUXILIARY, is_auxiliary=True, is_finite=True)
        self.words["is"] = Word(text="is", word_type=WordType.AUXILIARY, is_auxiliary=True, is_finite=True)
        self.words["are"] = Word(text="are", word_type=WordType.AUXILIARY, is_auxiliary=True, is_finite=True)
        self.words["have"] = Word(text="have", word_type=WordType.AUXILIARY, is_auxiliary=True, is_finite=False)
        self.words["has"] = Word(text="has", word_type=WordType.AUXILIARY, is_auxiliary=True, is_finite=True)
        
        # Negation
        self.words["not"] = Word(text="not", word_type=WordType.NEGATION, is_negation=True)
        
        # Nouns
        self.words["apple"] = Word(text="apple", word_type=WordType.NOUN, base_form="apple", plural_form="apples")
        self.words["apples"] = Word(text="apples", word_type=WordType.NOUN, base_form="apple", plural_form="apples", number="plural")
        self.words["book"] = Word(text="book", word_type=WordType.NOUN, base_form="book", plural_form="books")
        self.words["books"] = Word(text="books", word_type=WordType.NOUN, base_form="book", plural_form="books", number="plural")
        self.words["man"] = Word(text="man", word_type=WordType.NOUN, base_form="man", plural_form="men")
        self.words["men"] = Word(text="men", word_type=WordType.NOUN, base_form="man", plural_form="men", number="plural")
        
        # Articles
        self.words["a"] = Word(text="a", word_type=WordType.ARTICLE)
        self.words["an"] = Word(text="an", word_type=WordType.ARTICLE)
        self.words["the"] = Word(text="the", word_type=WordType.ARTICLE)
        
        # Adjectives
        self.words["good"] = Word(text="good", word_type=WordType.ADJECTIVE)
        self.words["red"] = Word(text="red", word_type=WordType.ADJECTIVE)
        
        # Adverbs
        self.words["quickly"] = Word(text="quickly", word_type=WordType.ADVERB)
        self.words["slowly"] = Word(text="slowly", word_type=WordType.ADVERB)
        
        # Time expressions
        self.words["yesterday"] = Word(text="yesterday", word_type=WordType.TIME_EXPRESSION)
        self.words["today"] = Word(text="today", word_type=WordType.TIME_EXPRESSION)
        self.words["tomorrow"] = Word(text="tomorrow", word_type=WordType.TIME_EXPRESSION)
        
        # Place expressions
        self.words["in the kitchen"] = Word(text="in the kitchen", word_type=WordType.PLACE_EXPRESSION)
        self.words["on the sofa"] = Word(text="on the sofa", word_type=WordType.PLACE_EXPRESSION)
    
    def _validate_subject_verb(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate subject-verb order."""
        subject_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.SUBJECT]
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB and word.is_finite]
        
        if not subject_indices or not verb_indices:
            return True, ""
        
        if subject_indices[0] < verb_indices[0]:
            return True, ""
        return False, "Subject should come before verb"
    
    def _validate_svo(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate SVO order."""
        subject_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.SUBJECT]
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB and word.is_finite]
        object_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.OBJECT]
        
        if not subject_indices or not verb_indices:
            return True, ""
        
        if subject_indices[0] >= verb_indices[0]:
            return False, "Subject should come before verb"
        
        if object_indices and verb_indices[0] >= object_indices[0]:
            return False, "Verb should come before object"
        
        return True, ""
    
    def _validate_question_auxiliary(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate question with auxiliary."""
        auxiliary_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.AUXILIARY]
        subject_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.SUBJECT]
        
        if not auxiliary_indices or not subject_indices:
            return True, ""
        
        if auxiliary_indices[0] < subject_indices[0]:
            return True, ""
        return False, "Auxiliary should come before subject in questions"
    
    def _validate_negation(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate negation."""
        auxiliary_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.AUXILIARY]
        negation_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.NEGATION]
        
        if not auxiliary_indices or not negation_indices:
            return True, ""
        
        if negation_indices[0] == auxiliary_indices[0] + 1:
            return True, ""
        return False, "'not' should come immediately after the auxiliary"
    
    def validate_sentence(self, sentence: List[Word]) -> Tuple[bool, List[str]]:
        """Validate a sentence against English grammar rules."""
        errors = []
        
        for rule_id, rule in self.rules.items():
            is_valid, error_msg = rule.validate(sentence)
            if not is_valid:
                errors.append(f"{rule.name}: {error_msg}")
        
        return len(errors) == 0, errors
    
    def generate_sentence(self, template_id: str = None, level: int = None) -> List[Word]:
        """Generate a random English sentence."""
        import random
        
        if template_id and template_id in self.templates:
            template = self.templates[template_id]
            return self._generate_from_template(template)
        
        if level:
            level_templates = self.get_templates_by_level(level)
            if level_templates:
                template = random.choice(level_templates)
                return self._generate_from_template(template)
        
        if self.templates:
            template = random.choice(list(self.templates.values()))
            return self._generate_from_template(template)
        
        return [self.words["i"], self.words["eat"], self.words["apple"]]
    
    def _generate_from_template(self, template: SentenceTemplate) -> List[Word]:
        """Generate a sentence from a template."""
        import random
        
        sentence = []
        for word_type in template.structure:
            candidates = self.get_words_by_type(word_type)
            if candidates:
                sentence.append(random.choice(candidates))
        
        return sentence
    
    def get_word_order(self, sentence_type: SentenceType = SentenceType.STATEMENT) -> List[WordType]:
        """Get the expected word order."""
        if sentence_type == SentenceType.QUESTION:
            return self.question_word_order
        return self.default_word_order
    
    def get_negation_word(self) -> str:
        """Get the English negation word."""
        return "not"
    
    def get_question_word(self, question_type: str = "yes_no") -> str:
        """Get English question words."""
        question_words = {
            "yes_no": "",
            "who": "who",
            "what": "what",
            "where": "where",
            "when": "when",
            "why": "why",
            "how": "how"
        }
        return question_words.get(question_type, "")
    
    def get_article(self, noun: Word) -> str:
        """Get the appropriate English article."""
        # Simplified - always use "a" for now
        return "a"

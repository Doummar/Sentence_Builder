"""
Danish Grammar implementation for Grammar Pro.

Implements all Danish-specific grammar rules, word order, and sentence patterns.
"""

from typing import Any, Dict, List, Optional, Tuple

from .base_grammar import (
    BaseGrammar,
    ClauseType,
    GrammarRule,
    SentenceTemplate,
    SentenceType,
    Word,
    WordType,
)


class DanishGrammar(BaseGrammar):
    """
    Danish grammar implementation.
    
    Implements Danish-specific rules including:
    - V2 word order rule
    - Subject-verb inversion in questions
    - Negation with "ikke"
    - Subordinate clause word order
    - Adjective agreement
    - Definite and indefinite articles
    """
    
    language_code = "da"
    language_name = "Danish"
    
    def __init__(self, settings=None):
        """Initialize Danish grammar."""
        # Define Danish word order patterns
        self.default_word_order = [
            WordType.SUBJECT,
            WordType.VERB,
            WordType.OBJECT,
            WordType.ADVERB,
            WordType.TIME_EXPRESSION,
            WordType.PLACE_EXPRESSION,
        ]
        
        self.question_word_order = [
            WordType.VERB,
            WordType.SUBJECT,
            WordType.OBJECT,
            WordType.ADVERB,
            WordType.TIME_EXPRESSION,
            WordType.PLACE_EXPRESSION,
        ]
        
        self.subordinate_clause_order = [
            WordType.SUBJECT,
            WordType.OBJECT,
            WordType.VERB,
            WordType.ADVERB,
            WordType.TIME_EXPRESSION,
            WordType.PLACE_EXPRESSION,
        ]
        
        super().__init__(settings)
    
    def _initialize_rules(self) -> None:
        """Initialize Danish grammar rules."""
        
        # Level 1: Subject + Verb
        self.rules["da_subject_verb"] = GrammarRule(
            rule_id="da_subject_verb",
            name="Subject + Verb Order",
            description="In Danish main clauses, the subject comes before the finite verb.",
            category="word_order",
            level=1,
            validation_func=self._validate_subject_verb_order,
            explanation="In Danish main clauses (statements), the basic word order is Subject-Verb-Object. "
                        "The subject always comes before the finite (conjugated) verb.",
            examples=[
                "Jeg spiser",  # I eat
                "Hun løber",   # She runs
                "De sover"    # They sleep
            ],
            counter_examples=[
                "Spiser jeg",  # Eat I (wrong)
                "Løber hun"   # Runs she (wrong)
            ]
        )
        
        # Level 2: Subject + Verb + Object
        self.rules["da_svo_order"] = GrammarRule(
            rule_id="da_svo_order",
            name="Subject-Verb-Object Order",
            description="In Danish main clauses, the basic order is Subject-Verb-Object.",
            category="word_order",
            level=2,
            validation_func=self._validate_svo_order,
            explanation="Danish follows the Subject-Verb-Object (SVO) pattern in main clauses. "
                        "This is the most common word order for simple statements.",
            examples=[
                "Jeg spiser æblet",  # I eat the apple
                "Hun læser bogen",   # She reads the book
                "De ser filmen"      # They watch the movie
            ],
            counter_examples=[
                "Jeg æblet spiser",  # I the apple eat (wrong)
                "Spiser jeg æblet"   # Eat I the apple (wrong - this would be a question)
            ]
        )
        
        # Level 7: Negation with "ikke"
        self.rules["da_negation_ikke"] = GrammarRule(
            rule_id="da_negation_ikke",
            name="Negation with 'ikke'",
            description="The negation 'ikke' comes after the finite verb in main clauses.",
            category="negation",
            level=7,
            validation_func=self._validate_negation_ikke,
            explanation="In Danish, the negation 'ikke' (not) is placed immediately after the finite verb. "
                        "This applies to both simple and compound tenses.",
            examples=[
                "Jeg spiser ikke",      # I do not eat
                "Hun løber ikke",       # She does not run
                "De har ikke set den"   # They have not seen it
            ],
            counter_examples=[
                "Jeg ikke spiser",      # I not eat (wrong)
                "Ikke jeg spiser"       # Not I eat (wrong)
            ]
        )
        
        # Level 8: Questions - Subject-Verb Inversion
        self.rules["da_question_inversion"] = GrammarRule(
            rule_id="da_question_inversion",
            name="Question Inversion",
            description="In yes/no questions, the verb comes before the subject.",
            category="questions",
            level=8,
            validation_func=self._validate_question_inversion,
            explanation="Danish yes/no questions use inversion: the finite verb comes before the subject. "
                        "This is different from statements where the subject comes first.",
            examples=[
                "Spiser du?",    # Do you eat? / Are you eating?
                "Løber hun?",    # Does she run? / Is she running?
                "Har de set den?" # Have they seen it?
            ],
            counter_examples=[
                "Du spiser?",    # You eat? (wrong for yes/no question)
                "Hun løber?"     # She runs? (wrong for yes/no question)
            ]
        )
        
        # Level 11: V2 Rule
        self.rules["da_v2_rule"] = GrammarRule(
            rule_id="da_v2_rule",
            name="V2 Rule",
            description="The finite verb is always in the second position in main clauses.",
            category="word_order",
            level=11,
            validation_func=self._validate_v2_rule,
            explanation="The V2 rule states that in Danish main clauses, the finite (conjugated) verb "
                        "must always be in the second position. The first position can be the subject "
                        "or any other element (adverb, object, etc.), but the verb is always second.",
            examples=[
                "Jeg spiser æblet",    # I eat the apple (Subject-Verb)
                "I går spiste jeg",     # Yesterday I ate (Adverb-Verb-Subject)
                "Bogen læser hun"       # The book reads she (Object-Verb-Subject)
            ],
            counter_examples=[
                "Jeg æblet spiser",     # I the apple eat (wrong - verb not in position 2)
                "I går jeg spiste"      # Yesterday I ate (wrong - verb not in position 2)
            ]
        )
        
        # Level 12: Subordinate Clause Word Order
        self.rules["da_subordinate_order"] = GrammarRule(
            rule_id="da_subordinate_order",
            name="Subordinate Clause Order",
            description="In subordinate clauses, the subject comes before the verb.",
            category="clauses",
            level=12,
            validation_func=self._validate_subordinate_order,
            explanation="Danish subordinate clauses (introduced by words like 'at', 'fordi', 'når') "
                        "have a different word order: Subject-Object-Verb. The finite verb comes at the end.",
            examples=[
                "Jeg ved, at hun spiser",      # I know that she eats
                "Han siger, at de kommer",     # He says that they are coming
                "Fordi jeg elsker dig"         # Because I love you
            ],
            counter_examples=[
                "Jeg ved, at spiser hun",      # I know that eats she (wrong)
                "Han siger, at kommer de"      # He says that are coming they (wrong)
            ]
        )
        
        # Level 13: Relative Clauses
        self.rules["da_relative_clause"] = GrammarRule(
            rule_id="da_relative_clause",
            name="Relative Clause Order",
            description="Relative clauses follow the subordinate clause word order.",
            category="clauses",
            level=13,
            validation_func=self._validate_relative_clause,
            explanation="Danish relative clauses (introduced by 'som', 'der', 'hvem') use the same "
                        "word order as subordinate clauses: Subject-Object-Verb.",
            examples=[
                "Manden, som spiser æblet",   # The man who eats the apple
                "Bogen, som hun læser",       # The book that she reads
                "Huset, der brændte"           # The house that burned
            ],
            counter_examples=[
                "Manden, som æblet spiser",   # The man who the apple eats (wrong)
            ]
        )
        
        # Adjective Agreement
        self.rules["da_adjective_agreement"] = GrammarRule(
            rule_id="da_adjective_agreement",
            name="Adjective Agreement",
            description="Adjectives agree with the noun in gender, number, and definiteness.",
            category="adjectives",
            level=3,
            validation_func=self._validate_adjective_agreement,
            explanation="In Danish, adjectives must agree with the noun they modify in gender (common/neuter), "
                        "number (singular/plural), and definiteness (indefinite/definite).",
            examples=[
                "en god mand"   # a good man (common, singular, indefinite)
                "et godt hus"   # a good house (neuter, singular, indefinite)
                "gode mænd"     # good men (plural)
                "den gode mand" # the good man (definite)
            ],
            counter_examples=[
                "en godt mand",  # a good man (wrong - should be 'god')
                "et god hus"     # a good house (wrong - should be 'godt')
            ]
        )
        
        # Definite vs Indefinite Articles
        self.rules["da_articles"] = GrammarRule(
            rule_id="da_articles",
            name="Articles",
            description="Danish uses 'en' for common gender and 'et' for neuter gender.",
            category="articles",
            level=1,
            validation_func=self._validate_articles,
            explanation="Danish has two indefinite articles: 'en' for common gender nouns and 'et' for neuter gender nouns. "
                        "There is no indefinite article in plural. The definite article is a suffix (-en, -et, -ne).",
            examples=[
                "en mand"   # a man (common)
                "et hus"   # a house (neuter)
                "mænd"     # men (plural, no article)
                "manden"   # the man (definite)
                "huset"    # the house (definite)
            ],
            counter_examples=[
                "et mand",   # a man (wrong - should be 'en')
                "en hus"     # a house (wrong - should be 'et')
            ]
        )
        
        # Time Expressions
        self.rules["da_time_expressions"] = GrammarRule(
            rule_id="da_time_expressions",
            name="Time Expression Placement",
            description="Time expressions can come before or after the verb in main clauses.",
            category="word_order",
            level=5,
            validation_func=self._validate_time_expressions,
            explanation="In Danish, time expressions (when something happens) can be placed either "
                        "before the subject (triggering V2 inversion) or after the verb.",
            examples=[
                "I går spiste jeg",   # Yesterday I ate (time before subject)
                "Jeg spiste i går"    # I ate yesterday (time after verb)
            ],
            counter_examples=[
                # Both orders are actually valid, so no counter-examples
            ]
        )
        
        # Place Expressions
        self.rules["da_place_expressions"] = GrammarRule(
            rule_id="da_place_expressions",
            name="Place Expression Placement",
            description="Place expressions typically come after time expressions.",
            category="word_order",
            level=6,
            validation_func=self._validate_place_expressions,
            explanation="In Danish, place expressions (where something happens) typically come after "
                        "time expressions and after the verb + object.",
            examples=[
                "Jeg spiser æblet i køkkenet",  # I eat the apple in the kitchen
                "I går spiste jeg æblet i køkkenet"  # Yesterday I ate the apple in the kitchen
            ]
        )
        
        # Modal Verbs
        self.rules["da_modal_verbs"] = GrammarRule(
            rule_id="da_modal_verbs",
            name="Modal Verb Position",
            description="Modal verbs come before the main verb in infinitive form.",
            category="verbs",
            level=9,
            validation_func=self._validate_modal_verbs,
            explanation="Danish modal verbs (kan, skal, vil, må, etc.) come before the main verb, "
                        "which is in its infinitive form (without 'at').",
            examples=[
                "Jeg kan spise",   # I can eat
                "Hun skal løbe",   # She must run
                "De vil komme"     # They want to come
            ],
            counter_examples=[
                "Jeg spise kan",   # I eat can (wrong)
            ]
        )
        
        # Perfect Tense
        self.rules["da_perfect_tense"] = GrammarRule(
            rule_id="da_perfect_tense",
            name="Perfect Tense Formation",
            description="Perfect tense is formed with 'har' or 'er' + past participle.",
            category="verbs",
            level=9,
            validation_func=self._validate_perfect_tense,
            explanation="The perfect tense in Danish is formed with the auxiliary 'har' (have) or 'er' (am/is/are) "
                        "plus the past participle of the main verb.",
            examples=[
                "Jeg har spist",   # I have eaten
                "Hun er løbet",    # She has run
                "De har set den"   # They have seen it
            ]
        )
    
    def _initialize_templates(self) -> None:
        """Initialize Danish sentence templates."""
        
        # Level 1: Subject + Verb
        self.templates["da_sv"] = SentenceTemplate(
            template_id="da_sv",
            name="Subject + Verb",
            structure=[WordType.SUBJECT, WordType.VERB],
            required_rules=["da_subject_verb"],
            level=1,
            category="basic",
            description="Simple sentences with subject and verb.",
            examples=["Jeg spiser", "Hun løber", "De sover"]
        )
        
        # Level 2: Subject + Verb + Object
        self.templates["da_svo"] = SentenceTemplate(
            template_id="da_svo",
            name="Subject + Verb + Object",
            structure=[WordType.SUBJECT, WordType.VERB, WordType.OBJECT],
            required_rules=["da_svo_order"],
            level=2,
            category="basic",
            description="Basic SVO sentences.",
            examples=["Jeg spiser æblet", "Hun læser bogen"]
        )
        
        # Level 3: Subject + Verb + Adjective + Object
        self.templates["da_sv_adj_o"] = SentenceTemplate(
            template_id="da_sv_adj_o",
            name="Subject + Verb + Adjective + Object",
            structure=[WordType.SUBJECT, WordType.VERB, WordType.ADJECTIVE, WordType.OBJECT],
            required_rules=["da_svo_order", "da_adjective_agreement"],
            level=3,
            category="adjectives",
            description="Sentences with adjectives modifying the object.",
            examples=["Jeg spiser det røde æble", "Hun læser den gode bog"]
        )
        
        # Level 5: Time Expressions
        self.templates["da_time_before"] = SentenceTemplate(
            template_id="da_time_before",
            name="Time Expression Before Subject",
            structure=[WordType.TIME_EXPRESSION, WordType.VERB, WordType.SUBJECT, WordType.OBJECT],
            required_rules=["da_v2_rule", "da_time_expressions"],
            level=5,
            category="time",
            description="Sentences with time expression before the subject (V2 inversion).",
            examples=["I går spiste jeg æblet", "I morgen vil hun læse bogen"]
        )
        
        self.templates["da_time_after"] = SentenceTemplate(
            template_id="da_time_after",
            name="Time Expression After Verb",
            structure=[WordType.SUBJECT, WordType.VERB, WordType.OBJECT, WordType.TIME_EXPRESSION],
            required_rules=["da_svo_order", "da_time_expressions"],
            level=5,
            category="time",
            description="Sentences with time expression after the verb.",
            examples=["Jeg spiste æblet i går", "Hun vil læse bogen i morgen"]
        )
        
        # Level 6: Place Expressions
        self.templates["da_place"] = SentenceTemplate(
            template_id="da_place",
            name="Place Expression",
            structure=[WordType.SUBJECT, WordType.VERB, WordType.OBJECT, WordType.PLACE_EXPRESSION],
            required_rules=["da_svo_order", "da_place_expressions"],
            level=6,
            category="place",
            description="Sentences with place expressions.",
            examples=["Jeg spiser æblet i køkkenet", "Hun læser bogen på sofaen"]
        )
        
        # Level 7: Negation
        self.templates["da_negation"] = SentenceTemplate(
            template_id="da_negation",
            name="Negation with 'ikke'",
            structure=[WordType.SUBJECT, WordType.VERB, WordType.NEGATION, WordType.OBJECT],
            required_rules=["da_negation_ikke"],
            level=7,
            category="negation",
            description="Sentences with negation using 'ikke'.",
            examples=["Jeg spiser ikke æblet", "Hun løber ikke hurtigt"]
        )
        
        # Level 8: Questions
        self.templates["da_question"] = SentenceTemplate(
            template_id="da_question",
            name="Yes/No Question",
            structure=[WordType.VERB, WordType.SUBJECT, WordType.OBJECT],
            required_rules=["da_question_inversion"],
            level=8,
            category="questions",
            description="Yes/no questions with subject-verb inversion.",
            examples=["Spiser du æblet?", "Løber hun hurtigt?"]
        )
        
        # Level 9: Modal Verbs
        self.templates["da_modal"] = SentenceTemplate(
            template_id="da_modal",
            name="Modal Verb",
            structure=[WordType.SUBJECT, WordType.MODAL, WordType.VERB, WordType.OBJECT],
            required_rules=["da_modal_verbs"],
            level=9,
            category="verbs",
            description="Sentences with modal verbs.",
            examples=["Jeg kan spise æblet", "Hun skal læse bogen"]
        )
        
        # Level 11: V2 with Adverb
        self.templates["da_v2_adverb"] = SentenceTemplate(
            template_id="da_v2_adverb",
            name="V2 with Adverb",
            structure=[WordType.ADVERB, WordType.VERB, WordType.SUBJECT, WordType.OBJECT],
            required_rules=["da_v2_rule"],
            level=11,
            category="word_order",
            description="Sentences with adverb in first position (V2 inversion).",
            examples=["Altid spiser jeg æblet", "Ofte løber hun i parken"]
        )
        
        # Level 12: Subordinate Clauses
        self.templates["da_subordinate"] = SentenceTemplate(
            template_id="da_subordinate",
            name="Subordinate Clause",
            structure=[
                WordType.SUBJECT, 
                WordType.VERB, 
                WordType.SUBORDINATING_CONJUNCTION,
                WordType.SUBJECT, 
                WordType.OBJECT, 
                WordType.VERB
            ],
            required_rules=["da_subordinate_order"],
            level=12,
            category="clauses",
            description="Main clause with subordinate clause.",
            examples=["Jeg ved, at hun spiser æblet", "Han siger, at de kommer i morgen"]
        )
        
        # Level 13: Relative Clauses
        self.templates["da_relative"] = SentenceTemplate(
            template_id="da_relative",
            name="Relative Clause",
            structure=[
                WordType.SUBJECT, 
                WordType.VERB, 
                WordType.OBJECT,
                WordType.RELATIVE_PRONOUN,
                WordType.SUBJECT, 
                WordType.OBJECT, 
                WordType.VERB
            ],
            required_rules=["da_relative_clause"],
            level=13,
            category="clauses",
            description="Sentences with relative clauses.",
            examples=["Jeg ser manden, som spiser æblet", "Hun læser bogen, som er god"]
        )
    
    def _initialize_words(self) -> None:
        """Initialize Danish word database."""
        
        # Pronouns
        self.words["jeg"] = Word(
            text="jeg",
            word_type=WordType.PRONOUN,
            base_form="jeg",
            person=1,
            number="singular"
        )
        self.words["du"] = Word(
            text="du",
            word_type=WordType.PRONOUN,
            base_form="du",
            person=2,
            number="singular"
        )
        self.words["han"] = Word(
            text="han",
            word_type=WordType.PRONOUN,
            base_form="han",
            person=3,
            number="singular"
        )
        self.words["hun"] = Word(
            text="hun",
            word_type=WordType.PRONOUN,
            base_form="hun",
            person=3,
            number="singular"
        )
        self.words["det"] = Word(
            text="det",
            word_type=WordType.PRONOUN,
            base_form="det",
            person=3,
            number="singular",
            gender="neuter"
        )
        self.words["vi"] = Word(
            text="vi",
            word_type=WordType.PRONOUN,
            base_form="vi",
            person=1,
            number="plural"
        )
        self.words["I"] = Word(
            text="I",
            word_type=WordType.PRONOUN,
            base_form="I",
            person=2,
            number="plural"
        )
        self.words["de"] = Word(
            text="de",
            word_type=WordType.PRONOUN,
            base_form="de",
            person=3,
            number="plural"
        )
        
        # Common verbs
        self.words["spiser"] = Word(
            text="spiser",
            word_type=WordType.VERB,
            base_form="spise",
            is_finite=True,
            past_tense="spiste"
        )
        self.words["spise"] = Word(
            text="spise",
            word_type=WordType.VERB,
            base_form="spise",
            is_finite=False
        )
        self.words["løber"] = Word(
            text="løber",
            word_type=WordType.VERB,
            base_form="løbe",
            is_finite=True,
            past_tense="løb"
        )
        self.words["løbe"] = Word(
            text="løbe",
            word_type=WordType.VERB,
            base_form="løbe",
            is_finite=False
        )
        self.words["læser"] = Word(
            text="læser",
            word_type=WordType.VERB,
            base_form="læse",
            is_finite=True,
            past_tense="læste"
        )
        self.words["læse"] = Word(
            text="læse",
            word_type=WordType.VERB,
            base_form="læse",
            is_finite=False
        )
        self.words["sover"] = Word(
            text="sover",
            word_type=WordType.VERB,
            base_form="sove",
            is_finite=True,
            past_tense="sov"
        )
        self.words["ser"] = Word(
            text="ser",
            word_type=WordType.VERB,
            base_form="se",
            is_finite=True,
            past_tense="så"
        )
        self.words["har"] = Word(
            text="har",
            word_type=WordType.AUXILIARY,
            base_form="have",
            is_finite=True,
            is_auxiliary=True
        )
        self.words["er"] = Word(
            text="er",
            word_type=WordType.AUXILIARY,
            base_form="være",
            is_finite=True,
            is_auxiliary=True
        )
        
        # Modal verbs
        self.words["kan"] = Word(
            text="kan",
            word_type=WordType.MODAL,
            base_form="kunne",
            is_finite=True,
            is_modal=True
        )
        self.words["skal"] = Word(
            text="skal",
            word_type=WordType.MODAL,
            base_form="skulle",
            is_finite=True,
            is_modal=True
        )
        self.words["vil"] = Word(
            text="vil",
            word_type=WordType.MODAL,
            base_form="ville",
            is_finite=True,
            is_modal=True
        )
        self.words["må"] = Word(
            text="må",
            word_type=WordType.MODAL,
            base_form="måtte",
            is_finite=True,
            is_modal=True
        )
        
        # Negation
        self.words["ikke"] = Word(
            text="ikke",
            word_type=WordType.NEGATION,
            is_negation=True
        )
        
        # Nouns
        self.words["æble"] = Word(
            text="æble",
            word_type=WordType.NOUN,
            base_form="æble",
            plural_form="æbler",
            gender="neuter"
        )
        self.words["æblet"] = Word(
            text="æblet",
            word_type=WordType.NOUN,
            base_form="æble",
            plural_form="æbler",
            gender="neuter"
        )
        self.words["bog"] = Word(
            text="bog",
            word_type=WordType.NOUN,
            base_form="bog",
            plural_form="bøger",
            gender="common"
        )
        self.words["bogen"] = Word(
            text="bogen",
            word_type=WordType.NOUN,
            base_form="bog",
            plural_form="bøger",
            gender="common"
        )
        self.words["mand"] = Word(
            text="mand",
            word_type=WordType.NOUN,
            base_form="mand",
            plural_form="mænd",
            gender="common"
        )
        self.words["manden"] = Word(
            text="manden",
            word_type=WordType.NOUN,
            base_form="mand",
            plural_form="mænd",
            gender="common"
        )
        self.words["hus"] = Word(
            text="hus",
            word_type=WordType.NOUN,
            base_form="hus",
            plural_form="huse",
            gender="neuter"
        )
        self.words["huset"] = Word(
            text="huset",
            word_type=WordType.NOUN,
            base_form="hus",
            plural_form="huse",
            gender="neuter"
        )
        self.words["film"] = Word(
            text="film",
            word_type=WordType.NOUN,
            base_form="film",
            plural_form="film",
            gender="common"
        )
        self.words["filmen"] = Word(
            text="filmen",
            word_type=WordType.NOUN,
            base_form="film",
            plural_form="film",
            gender="common"
        )
        
        # Articles
        self.words["en"] = Word(
            text="en",
            word_type=WordType.ARTICLE,
            base_form="en"
        )
        self.words["et"] = Word(
            text="et",
            word_type=WordType.ARTICLE,
            base_form="et"
        )
        
        # Adjectives
        self.words["god"] = Word(
            text="god",
            word_type=WordType.ADJECTIVE,
            base_form="god"
        )
        self.words["gode"] = Word(
            text="gode",
            word_type=WordType.ADJECTIVE,
            base_form="god"
        )
        self.words["godt"] = Word(
            text="godt",
            word_type=WordType.ADJECTIVE,
            base_form="god"
        )
        self.words["rød"] = Word(
            text="rød",
            word_type=WordType.ADJECTIVE,
            base_form="rød"
        )
        self.words["røde"] = Word(
            text="røde",
            word_type=WordType.ADJECTIVE,
            base_form="rød"
        )
        self.words["rødt"] = Word(
            text="rødt",
            word_type=WordType.ADJECTIVE,
            base_form="rød"
        )
        
        # Adverbs
        self.words["hurtigt"] = Word(
            text="hurtigt",
            word_type=WordType.ADVERB,
            base_form="hurtigt"
        )
        self.words["langsomt"] = Word(
            text="langsomt",
            word_type=WordType.ADVERB,
            base_form="langsomt"
        )
        self.words["altid"] = Word(
            text="altid",
            word_type=WordType.ADVERB,
            base_form="altid"
        )
        self.words["ofte"] = Word(
            text="ofte",
            word_type=WordType.ADVERB,
            base_form="ofte"
        )
        
        # Time expressions
        self.words["i går"] = Word(
            text="i går",
            word_type=WordType.TIME_EXPRESSION,
            base_form="i går"
        )
        self.words["i morgen"] = Word(
            text="i morgen",
            word_type=WordType.TIME_EXPRESSION,
            base_form="i morgen"
        )
        self.words["idag"] = Word(
            text="idag",
            word_type=WordType.TIME_EXPRESSION,
            base_form="idag"
        )
        
        # Place expressions
        self.words["i køkkenet"] = Word(
            text="i køkkenet",
            word_type=WordType.PLACE_EXPRESSION,
            base_form="i køkkenet"
        )
        self.words["på sofaen"] = Word(
            text="på sofaen",
            word_type=WordType.PLACE_EXPRESSION,
            base_form="på sofaen"
        )
        self.words["i parken"] = Word(
            text="i parken",
            word_type=WordType.PLACE_EXPRESSION,
            base_form="i parken"
        )
        
        # Subordinating conjunctions
        self.words["at"] = Word(
            text="at",
            word_type=WordType.SUBORDINATING_CONJUNCTION,
            base_form="at"
        )
        self.words["fordi"] = Word(
            text="fordi",
            word_type=WordType.SUBORDINATING_CONJUNCTION,
            base_form="fordi"
        )
        self.words["når"] = Word(
            text="når",
            word_type=WordType.SUBORDINATING_CONJUNCTION,
            base_form="når"
        )
        
        # Relative pronouns
        self.words["som"] = Word(
            text="som",
            word_type=WordType.RELATIVE_PRONOUN,
            base_form="som"
        )
        self.words["der"] = Word(
            text="der",
            word_type=WordType.RELATIVE_PRONOUN,
            base_form="der"
        )
        self.words["hvem"] = Word(
            text="hvem",
            word_type=WordType.RELATIVE_PRONOUN,
            base_form="hvem"
        )
    
    # Validation functions for Danish rules
    
    def _validate_subject_verb_order(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate that subject comes before verb in main clauses."""
        subject_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.SUBJECT]
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB and word.is_finite]
        
        if not subject_indices or not verb_indices:
            return True, ""  # Can't validate without subject or verb
        
        first_subject = subject_indices[0]
        first_verb = verb_indices[0]
        
        if first_subject < first_verb:
            return True, ""
        else:
            return False, f"Subject '{sentence[first_subject].text}' should come before verb '{sentence[first_verb].text}'"
    
    def _validate_svo_order(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate SVO order."""
        subject_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.SUBJECT]
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB and word.is_finite]
        object_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.OBJECT]
        
        if not subject_indices or not verb_indices:
            return True, ""
        
        first_subject = subject_indices[0]
        first_verb = verb_indices[0]
        
        if first_subject >= first_verb:
            return False, f"Subject should come before verb"
        
        if object_indices:
            first_object = object_indices[0]
            if first_verb >= first_object:
                return False, f"Verb should come before object"
        
        return True, ""
    
    def _validate_negation_ikke(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate that 'ikke' comes after the finite verb."""
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB and word.is_finite]
        negation_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.NEGATION]
        
        if not verb_indices or not negation_indices:
            return True, ""
        
        first_verb = verb_indices[0]
        first_negation = negation_indices[0]
        
        if first_negation == first_verb + 1:
            return True, ""
        elif first_negation < first_verb:
            return False, f"'ikke' should come after the verb, not before"
        else:
            return False, f"'ikke' should come immediately after the verb"
    
    def _validate_question_inversion(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate that verb comes before subject in questions."""
        subject_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.SUBJECT]
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB and word.is_finite]
        
        if not subject_indices or not verb_indices:
            return True, ""
        
        first_subject = subject_indices[0]
        first_verb = verb_indices[0]
        
        if first_verb < first_subject:
            return True, ""
        else:
            return False, f"In questions, the verb should come before the subject"
    
    def _validate_v2_rule(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate that the finite verb is in the second position."""
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB and word.is_finite]
        
        if not verb_indices:
            return True, ""
        
        first_verb = verb_indices[0]
        
        if first_verb == 1:  # Second position (0-indexed)
            return True, ""
        else:
            return False, f"The finite verb should be in the second position, but it's in position {first_verb + 1}"
    
    def _validate_subordinate_order(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate subordinate clause word order (subject before verb)."""
        # This is a simplified validation
        # In a real implementation, we'd need to identify the subordinate clause
        subject_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.SUBJECT]
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB and word.is_finite]
        
        if not subject_indices or not verb_indices:
            return True, ""
        
        # In subordinate clauses, subject should come before verb
        first_subject = subject_indices[0]
        first_verb = verb_indices[0]
        
        if first_subject < first_verb:
            return True, ""
        else:
            return False, "In subordinate clauses, the subject should come before the verb"
    
    def _validate_relative_clause(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate relative clause word order."""
        # Similar to subordinate clause
        return self._validate_subordinate_order(sentence)
    
    def _validate_adjective_agreement(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate adjective agreement with nouns."""
        # This is a simplified validation
        # In a real implementation, we'd check that adjectives match their nouns
        return True, ""
    
    def _validate_articles(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate article usage."""
        # Simplified validation
        return True, ""
    
    def _validate_time_expressions(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate time expression placement."""
        # Both before and after are valid in Danish
        return True, ""
    
    def _validate_place_expressions(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate place expression placement."""
        return True, ""
    
    def _validate_modal_verbs(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate modal verb position."""
        modal_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.MODAL]
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB and not word.is_finite]
        
        if not modal_indices or not verb_indices:
            return True, ""
        
        first_modal = modal_indices[0]
        first_verb = verb_indices[0]
        
        if first_modal < first_verb:
            return True, ""
        else:
            return False, "Modal verb should come before the main verb"
    
    def _validate_perfect_tense(self, sentence: List[Word]) -> Tuple[bool, str]:
        """Validate perfect tense formation."""
        auxiliary_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.AUXILIARY]
        verb_indices = [i for i, word in enumerate(sentence) if word.word_type == WordType.VERB]
        
        if not auxiliary_indices or len(verb_indices) < 2:
            return True, ""
        
        first_auxiliary = auxiliary_indices[0]
        
        # Check if there's a verb after the auxiliary
        for i in range(first_auxiliary + 1, len(sentence)):
            if sentence[i].word_type == WordType.VERB:
                return True, ""
        
        return False, "Auxiliary verb should be followed by a main verb"
    
    def validate_sentence(self, sentence: List[Word]) -> Tuple[bool, List[str]]:
        """
        Validate a sentence against all applicable Danish grammar rules.
        
        Args:
            sentence: List of Word objects
            
        Returns:
            Tuple of (is_valid, list_of_error_messages)
        """
        errors = []
        
        # Check all rules
        for rule_id, rule in self.rules.items():
            is_valid, error_msg = rule.validate(sentence)
            if not is_valid:
                errors.append(f"{rule.name}: {error_msg}")
        
        return len(errors) == 0, errors
    
    def generate_sentence(self, template_id: str = None, level: int = None) -> List[Word]:
        """
        Generate a random Danish sentence.
        
        Args:
            template_id: Optional template ID to use
            level: Optional difficulty level
            
        Returns:
            List of Word objects forming a valid sentence
        """
        import random
        
        # If template_id is specified, use that template
        if template_id and template_id in self.templates:
            template = self.templates[template_id]
            return self._generate_from_template(template)
        
        # If level is specified, choose a random template from that level
        if level:
            level_templates = self.get_templates_by_level(level)
            if level_templates:
                template = random.choice(level_templates)
                return self._generate_from_template(template)
        
        # Otherwise, choose a random template
        if self.templates:
            template = random.choice(list(self.templates.values()))
            return self._generate_from_template(template)
        
        # Fallback: return a simple sentence
        return [
            self.words["jeg"],
            self.words["spiser"],
            self.words["æblet"]
        ]
    
    def _generate_from_template(self, template: SentenceTemplate) -> List[Word]:
        """Generate a sentence from a template."""
        import random
        
        sentence = []
        
        for word_type in template.structure:
            # Get all words of this type
            candidates = self.get_words_by_type(word_type)
            
            if candidates:
                # Choose a random word
                word = random.choice(candidates)
                sentence.append(word)
            else:
                # If no words of this type, skip or use a default
                # For now, we'll just skip
                pass
        
        return sentence
    
    def get_word_order(self, sentence_type: SentenceType = SentenceType.STATEMENT) -> List[WordType]:
        """
        Get the expected word order for a sentence type.
        
        Args:
            sentence_type: Type of sentence
            
        Returns:
            List of WordType in expected order
        """
        if sentence_type == SentenceType.QUESTION:
            return self.question_word_order
        elif sentence_type == SentenceType.STATEMENT:
            return self.default_word_order
        else:
            return self.default_word_order
    
    def get_negation_word(self) -> str:
        """Get the Danish negation word."""
        return "ikke"
    
    def get_question_word(self, question_type: str = "yes_no") -> str:
        """Get Danish question words."""
        question_words = {
            "yes_no": "",
            "who": "hvem",
            "what": "hvad",
            "where": "hvor",
            "when": "hvornår",
            "why": "hvorfor",
            "how": "hvordan"
        }
        return question_words.get(question_type, "")
    
    def get_article(self, noun: Word) -> str:
        """
        Get the appropriate Danish article for a noun.
        
        Args:
            noun: The noun
            
        Returns:
            The article ('en', 'et', or empty string)
        """
        if noun.gender == "common":
            return "en"
        elif noun.gender == "neuter":
            return "et"
        return ""
    
    def shutdown(self) -> None:
        """Clean up resources."""
        pass

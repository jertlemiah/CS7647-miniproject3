from ast import List
from dataclasses import dataclass
from enum import Enum
from typing import List

class POS(Enum):
    ADJ = 0 #adjective
    ADP = 1 #adposition
    ADV = 2 #adverb
    AUX = 3 #auxiliary
    CCONJ = 4 #coordinating conjunction
    DET = 5 #determiner
    INTJ = 6 #interjection
    NOUN = 7 #noun
    NUM = 8 #numeral
    PART = 9 #particle
    PRON = 10 #pronoun
    PROPN = 11 #proper noun
    PUNCT = 12 #punctuation
    SCONJ = 13 #subordinating conjunction
    SYM = 14 #symbol
    VERB = 15 #verb
    X = 16 #other
    TIME = 17
    DIST = 18
    ART = 19

class RELATION(Enum):
    SUBJECT = 0
    VERB = 1 #adposition
    DIRECTOBJ = 2
    INDIRECTOBJ = 3
    PREP = 4
    DIST = 5
    TIME = 6

@dataclass
class Phrase():
    text: str
    words: list
    relation: RELATION


@dataclass
class Word():
    text: str
    lemma: str
    posList: List[POS]
    isStop: bool

# @dataclass
# class Time:Word():

@dataclass
class Sentence():
    text: str
    words: List[Word]
    phrases: List[Phrase]
    subjectPhrase: Phrase
    verbPhrase: Phrase
    nonStopWords: List[Word]
    mentionsTime: bool
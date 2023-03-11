from dataclasses import dataclass
from enum import Enum


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

@dataclass
class Word():
    text: list[str]
    lemma: str
    pos: list[POS]
    isStop: bool

# @dataclass
# class Time:Word():

@dataclass
class Sentence():
    raw: str
    modified: str
    words: list[Word]
    subject: list[str]
    primaryVerb: Word
    directObject: list[str]
    indirectObject: list[str]
    mentionsTime: bool
    predicateNom: str
    predicateAdj: str
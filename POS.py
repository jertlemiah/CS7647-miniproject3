from dataclasses import dataclass
from enum import Enum
# from typing import List

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
    text: str#List[str]
    lemma: str
    posList: list#List[POS]
    isStop: bool

# @dataclass
# class Time:Word():

@dataclass
class Sentence():
    raw: str
    modified: str
    words: list#List[Word]
    subject: list#List[str]
    primaryVerb: Word
    directObject: list#List[str]
    indirectObject: list#List[str]
    mentionsTime: bool
    predicateNom: str
    predicateAdj: str
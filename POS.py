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

class Word():
    text: str
    pos: POS
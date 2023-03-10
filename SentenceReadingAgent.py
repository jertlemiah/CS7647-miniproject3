from dataclasses import dataclass
from enum import Enum
from POS import POS
from PreprocessingDict import PreprocessingDict
# import json


class SentenceReadingAgent:
    wordDict:dict
    
    def __init__(self):
        #If you want to do any initial processing, add it here.
        # with open("preprocessing.json") as json_file:
            # self.wordDict = json.load(json_file)
        self.wordDict = PreprocessingDict.wordDict
        pass

    THE_FIVE_WS = ["who", "what", "when", "where", "why", "how"]

    def solve(self, sentence, question):
        #Add your code here! Your solve method should receive
		#two strings as input: sentence and question. It should
		#return a string representing the answer to the question.
        print(f"sentence: '{sentence}'")
        print(f"question: '{question}'")
        self.parseSentence(sentence=sentence)

        for questionWord in self.THE_FIVE_WS:
            if questionWord in question.lower():
                print(f"question word: {questionWord}")
        pass

    def parseSentence(self, sentence):
        wordStrings = sentence.replace('.','').split()
        # sentence = Sentence(None)
        words = []
        # subjects = []
        # verbs = []
        for string in wordStrings:
            try:
                word = self.wordDict[string]
                words.append(word)
                # if word["pos"][0] == POS.VERB:
                #     verbs.append(string)
            except:
                pass
            # if "VERB" in word["pos"]:
            #     verbs.append(string)
            # match word["pos"][0]:
            #     case POS.NOUN:
            #         subjects.append(word)
            #         pass
            #     case POS.PRON:
            #         subjects.append(word)
            #         pass
            #     case POS.PROPN:
            #         subjects.append(word)
            #         pass

            #     case POS.ADJ:
            #         pass

            #     case POS.VERB:
            #         pass

                
            #     case POS.ADP:
            #         pass
            #     case POS.ADV:
            #         pass
            #     case POS.CCONJ:
            #         pass
            #     case POS.DET:
            #         pass
            #     case POS.INTJ:
            #         pass
                
            #     case POS.NUM:
            #         pass
            #     case POS.PART:
            #         pass
                
            #     case POS.PUNCT:
            #         pass
            #     case POS.SCONJ:
            #         pass
            #     case POS.SYM:
            #         pass
                
            #     case _:#POS.X:
            #         pass

        
        # sentence.verb = 
        verb = [x for x in words if POS.VERB in x['pos']]
        # parts = sentence.split(verbs[0])
        # subject = parts[0]
        # complement = parts[1]
        pos = words.index(verb[0])
        subjectList = words[:pos]
        complementList = words[pos+1:]



        

        pass

    def Find_Who(sentence):

        pass
    
    def Find_What(sentence):
        pass

    def Find_When(sentence):
        pass

    def Find_Where(sentence):
        pass

    def Find_Why(sentence):
        pass

    def Find_How(sentence):
        pass


@dataclass
class Noun():
    adj: list[str]

@dataclass
class PartOfSpeach():
    pos: str



@dataclass
class Sentence():
    raw: str
    # words:
    subject: list[str]
    primaryVerb: str
    directObject: str
    indirectObject: str
    predicateNom: str
    predicateAdj: str

# @dataclass
# class Sentence():
#     subject: str

# adjectives
# adverbs
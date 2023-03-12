from dataclasses import dataclass
from enum import Enum
from POS import POS
from POS import Word
from POS import Sentence
from POS import Phrase
from POS import RELATIONSHIP
from PreprocessingDict import PreprocessingDict
from datetime import datetime
# from typing import List
import re
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
        try:
            print(f"sentence: '{sentence}'")
            print(f"question: '{question}'")
            formattedSentence = self.parseSentence(sentenceRaw=sentence)
            formattedQuestion = self.parseSentence(sentenceRaw=question.replace("?",""))

            for questionWord in self.THE_FIVE_WS:
                if questionWord in question.lower():
                    i = [x for x in formattedQuestion.words if x.text == questionWord]
                    # secondaryWord = formattedQuestion.words[i+1]
                    secondaryWord = formattedQuestion.primaryVerb
                    # print(f"question word: {questionWord}, secondary word: {secondaryWord.text}")
                    break
        
            answer = ""
            if questionWord == "who":
                # if sentence ends with ADP, then it's probably actually a Whom
                # if POS.ADP in formattedQuestion.words[-1].posList and formattedQuestion.words[-1].text != "with":
                if any(pos.value in {POS.ADP.value} for pos in formattedQuestion.words[-1].posList) and formattedQuestion.words[-1].text != "with":
                    answer = self.Find_Whom(formattedSentence, formattedQuestion)
                else:
                    answer = self.Find_Who(formattedSentence, formattedQuestion)
            elif questionWord == "what":
                if formattedQuestion.mentionsTime:
                    answer = self.Find_When(formattedSentence, formattedQuestion)
                else:
                    answer = self.Find_What(formattedSentence, formattedQuestion)
            elif questionWord == "when":
                answer = self.Find_When(formattedSentence, formattedQuestion)
            elif questionWord == "where":
                answer = self.Find_Where(formattedSentence, formattedQuestion)
            elif questionWord == "why":
                answer = self.Find_Why(formattedSentence, formattedQuestion)
            elif questionWord == "how":
                answer = self.Find_How(formattedSentence, formattedQuestion)
            return answer
        except:
            return None


    def parseSentence(self, sentenceRaw):
        wordStrings = sentenceRaw.replace('.','').split()
        # sentence = Sentence(None)
        words = []
        # subjects = []
        # verbs = []
        for string in wordStrings:
            try:
                word = self.wordDict[string.lower()]
                # if word["pos"][0] == POS.VERB:
                #     verbs.append(string)
            except:
                regexPattern = '\d:\d\d.*'
                if re.search(regexPattern, string) != None:
                    word = Word(
                        text = string,
                        lemma = string,
                        posList = {POS.TIME},
                        isStop = False
                    )
                else:
                    word = Word(
                        text = string,
                        lemma = string,
                        posList = {POS.X},
                        isStop = False
                    )
            word.text.replace("?","").replace(",","")
            words.append(word)
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

        modifiedSentence = ""
        modifiedWords = []
        for word in words:
            temp = word.text
            if not word.isStop: #any(x in word.posList for x in {POS.VERB, POS.ADJ, POS.ADV, POS.NOUN, POS.TIME, POS.PRON, POS.PROPN,}):

                temp = f"{'/'.join(pos.name for pos in word.posList)}"
                # temp = word.posList.name
            modifiedWords.append(temp)
        modifiedSentence = " ".join(modifiedWords)
        # print(modifiedSentence)


        # sentence.verb =
        # for word in words:
        #     if
        verb = [word for word in words for pos in word.posList if pos.value == POS.VERB.value]
        # parts = sentence.split(verbs[0])
        # subject = parts[0]
        # complement = parts[1]
        # words = list(filter(lambda word: not word.isStop, words))
        verbIndex = words.index(verb[0])
        # subjects = list(filter(lambda word: any(pos.value in {POS.PRON.value, POS.PROPN.value, POS.NOUN.value} for pos in word.posList), words[:verbIndex]))
        subjects = list(filter(lambda word: not word.isStop and IsWordAnyPos(word, {POS.PRON.value, POS.PROPN.value, POS.NOUN.value}), words[:verbIndex]))
        # # subjects = list(filter(lambda word: any(pos in {POS.PRON, POS.PROPN} for pos in word.posList), words[:i]))
        # indirectObjects = list(filter(lambda word: any(pos.value in {POS.PRON.value, POS.PROPN.value} for pos in word.posList), words[verbIndex:]))
        # # complementList = words[i+1:]
        # directObjects = list(filter(lambda word: any(pos.value in {POS.NOUN.value} for pos in word.posList), words[verbIndex:]))
        # # two things:
        
        
        indirectObjects = []
        directObjects = []
        prepFound = False
        collectingIndirect = True
        collectingDirect = False
        objIndex = verbIndex
        for i in range(verbIndex+1, len(words)):
            word = words[i]
            
            # if any(pos.value in {POS.ADP.value} for pos in word.posList):
            if IsWordAnyPos(word, {POS.ADP.value}):
                if collectingDirect:
                    break
                else:
                    prepFound = True
                    continue

            elif IsWordAnyPos(word, {POS.ADJ.value}):
                continue

            # elif not prepFound and collectingIndirect and any(pos.value in {POS.PRON.value, POS.PROPN.value, POS.NOUN.value} for pos in word.posList):
            elif not prepFound and collectingIndirect and IsWordAnyPos(word, {POS.PRON.value, POS.PROPN.value, POS.NOUN.value}):
                if not word.isStop:
                    indirectObjects.append(word)

            elif word.text == "and":
                continue

            elif collectingIndirect:
                collectingIndirect = False
                collectingDirect = True
            
            elif collectingDirect and any(pos.value in {POS.PRON.value, POS.PROPN.value, POS.NOUN.value} for pos in word.posList):
                directObjects.append(word)
                objIndex = i

            else:
                break    
        

        for i in range(objIndex+1, len(words)):
            word = words[i]
            if IsWordAnyPos(word, {POS.PROPN.value}) and IsWordAnyPos(words[i-1], {POS.ADP.value}) :
                indirectObjects.append(word)
            pass
        
        phrases = []
        wordsInPhrase = []
        # for i in range(len(words)):
        i = 0

        # Find the subject
        wordsInPhrase = []
        for i in range(i, len(words)):
            word = words[i]
            if not IsWordAnyPos(word, {POS.VERB.value, POS.ADV.value}):
                wordsInPhrase.append(word)
            else:
                newPhrase = Phrase(
                    text = " ".join(word.text for word in wordsInPhrase),
                    words = wordsInPhrase,
                    rel = RELATIONSHIP.SUBJECT
                )
                phrases.append(newPhrase)
                break

        # Find the verb  
        wordsInPhrase = []
        for i in range(i, len(words)):
            word = words[i]
            if IsWordAnyPos(word, {POS.VERB.value, POS.ADV.value}):
                wordsInPhrase.append(word)
            else:
                newPhrase = Phrase(
                    text = " ".join(word.text for word in wordsInPhrase),
                    words = wordsInPhrase,
                    rel = RELATIONSHIP.VERB
                )
                phrases.append(newPhrase)
                break
        
        # Find the Indirect Object, if any
        if IsWordAnyPos(word, {POS.PRON.value, POS.PROPN.value}): 
            wordsInPhrase = []
            for i in range(i, len(words)):
                word = words[i]
                if IsWordAnyPos(word, {POS.PRON.value, POS.PROPN.value, POS.NOUN.value}):
                    wordsInPhrase.append(word)
                else:
                    newPhrase = Phrase(
                        text = " ".join(word.text for word in wordsInPhrase),
                        words = wordsInPhrase,
                        rel = RELATIONSHIP.INDIRECTOBJ
                    )
                    phrases.append(newPhrase)
                    break
                    
        # Find the Direct Object, if any
        if not IsWordAnyPos(word, {POS.ADP.value}):
            wordsInPhrase = []
            for i in range(i, len(words)):
                word = words[i]
                if not IsWordAnyPos(word, {POS.ADP.value}):
                    wordsInPhrase.append(word)
                else:
                    newPhrase = Phrase(
                        text = " ".join(word.text for word in wordsInPhrase),
                        words = wordsInPhrase,
                        rel = RELATIONSHIP.DIRECTOBJ
                    )
                    phrases.append(newPhrase)
                    break

        # Find all propositional & other phrases
        while i < len(words):
            wordsInPhrase = [word]
            i = i + 1
            needToBreak = False
            for i in range(i, len(words)):
                word = words[i]
                if IsWordAnyPos(word, {POS.ADP.value, POS.SCONJ.value}) or word.text == "every":
                    needToBreak = True
                    
                else:
                    wordsInPhrase.append(word)
                
                if i+1 == len(words) or needToBreak:
                    newPhrase = Phrase(
                        text = " ".join(word.text for word in wordsInPhrase),
                        words = wordsInPhrase,
                        rel = RELATIONSHIP.DIRECTOBJ
                    )
                    phrases.append(newPhrase)
                    break
                #     i = i + 1
                #     word = words[i]
                #     if IsWordAnyPos(word, {POS.PRON.value, POS.PROPN.value, POS.NOUN.value}):
                #         newPhrase = Phrase(
                #             text = " ".join(word.text for word in wordsInPhrase),
                #             words = wordsInPhrase,
                #             rel = RELATIONSHIP.PREP
                #         )
                #         phrases.append(newPhrase)
                #         break

        
        # while i < len(words):
        #     word = words[i]

        #     # everything before the adverb / verb is the subject
        #     # if no preposition, then the first thing you encounter is the indirect object
        #     # indirect objects are only placed directly after a verb and before a direct object
            
        #     if len(phrases) == 0: # Find Subject
                
                            
        #     else: # Then it is 

        #         i = i + 1
                


        #     pass

        mentionsTime = "time" in sentenceRaw.lower()

        nonStopWords = list(filter(lambda word: not word.isStop, words))

        sentence = Sentence(
            raw = sentenceRaw,
            modified = modifiedSentence,
            words = words,
            nonStopWords = nonStopWords,
            subject = subjects,
            primaryVerb = verb[0],
            directObject = directObjects,
            indirectObject = indirectObjects,
            mentionsTime = mentionsTime,
            predicateAdj = None,
            predicateNom = None

        )
        return sentence

    def Find_Who(self, sentence:Sentence, question:Sentence):
        # looking for a propernoun
        # verb = [x for x in words if POS.VERB in x.pos]
        # words = list(filter(lambda word: not word.isStop, words))
        # i = words.index(verb[0])
        # subjectPronouns = words[:i]

        if question.words[-1].text == "with" or "with" in sentence.raw:
            names = []
            propernounsInQuestion = list(filter(lambda word: any(pos.value in {POS.PROPN.value, POS.PRON.value, POS.NOUN.value} for pos in word.posList), question.words))
            for person in sentence.subject:
                if person not in propernounsInQuestion:
                    names.append(person.text)
            answer = " and ".join(names)
            # list(filter(lambda word: any(name in question.subject for name in sentence.subject), sentence.subject))[0]
            # answer = any(name not in sentence.subject for name in question.subject).text
        else:
            names = []
            for person in sentence.subject:
                names.append(person.text)
            answer = " and ".join(names)


        return answer

    def Find_Whom(self, sentence:Sentence, question:Sentence):
        # if sentence ends with ADP, then it's a Whom

        # looking for a propernoun

        # verb = [x for x in words if POS.VERB in x.pos]
        # words = list(filter(lambda word: not word.isStop, words))
        # i = words.index(verb[0])
        # subjectPronouns = words[:i]
        names = []
        # propernounsInQuestion = list(filter(lambda word: any(pos in {POS.PROPN} for pos in word.posList), question.words))
        for person in sentence.indirectObject:
            if any(pos.value in {POS.PROPN.value} for pos in person.posList):
                names.append(person.text)
        answer = " and ".join(names)
        # answer = " and ".join(sentence.indirectObject)


        return answer

    def Find_What(self, sentence:Sentence, question:Sentence):
        if question.words[1].text == "did":
            return sentence.directObject[0].text
        else:
            return self.Find_Who(sentence, question)
        pass

    def Find_When(self, sentence:Sentence, question:Sentence):
        time = [word for word in sentence.words for pos in word.posList if pos.value == POS.TIME.value][0]
        # time = [word for word in sentence.words if POS.TIME in word.posList][0]
        return time.text

    def Find_Where(self, sentence:Sentence, question:Sentence):
        # I need to find "to <noun>"
        indices = [i for i in range(len(sentence.words)) if sentence.words[i].text == "to"]
        # i = sentence.words.index(self.wordDict["to"])
        for i in indices:
            for j in range(i, len(sentence.words)):
                nextWord = sentence.words[j]
                if any(pos.value in {POS.NOUN.value} for pos in nextWord.posList):
                    return nextWord.text
                elif any(pos.value in {POS.VERB.value} for pos in nextWord.posList):
                    break
        
         # I need to find "from ... <noun>"
        indices = [i for i in range(len(sentence.words)) if sentence.words[i].text == "from"]
        # i = sentence.words.index(self.wordDict["to"])
        for i in indices:
            for j in range(i, len(sentence.words)):
                nextWord = sentence.words[j]
                if any(pos.value in {POS.NOUN.value} for pos in nextWord.posList):
                    return nextWord.text
                elif any(pos.value in {POS.VERB.value} for pos in nextWord.posList):
                    break
        return None

    def Find_Why(self, sentence:Sentence, question:Sentence):
        pass

    def Find_How(self, sentence:Sentence, question:Sentence):
        
        # if any(pos.value in {POS.ADJ.value} for pos in sentence.words[1].posList):
        if IsWordAnyPos(question.words[1], {POS.ADJ.value}):
            obj = question.indirectObject[0]

        # if POS.ADJ in question.words[1].pos:
            # obj = question.directObject[0]
            i = sentence.words.index(obj)
            if IsWordAnyPos(sentence.words[i-1], {POS.ADJ.value}):
                return sentence.words[i-1].text
            else:
                return None
        elif question.words[1].text == "far" or question.words[1].text == "long":
            # dist = [word for word in sentence.words if POS.DIST in word.posList][0]
            dist = [word for word in sentence.words for pos in word.posList if pos.value == POS.DIST.value][0]
            answer = dist.text
            i = sentence.words.index(dist)
            num = sentence.words[i-1]
            # if (num.pos.value == POS.NUM.value):
            if any(pos.value in {POS.NUM.value} for pos in num.posList) and num.text != "one":
                answer = num.text + " " + answer
                
            return answer
        elif question.words[1].text == "long":
            # need to figure out how to differentiate between time and distance
            pass
        elif question.words[1].text in {"does","do"}:
            return sentence.primaryVerb.text
            pass
        pass

def IsWordAnyPos(word: Word, lst:list ):
    return any(pos.value in lst for pos in word.posList)

# @dataclass
# class Noun():
#     adj: List[str]

# @dataclass
# class PartOfSpeach():
#     pos: str



# @dataclass
# class Verb():
#     word: Word
#     directObject: str
#     indirectObject: str
#     adverb: Word

# @dataclass
# class Sentence():
#     subject: str

# adjectives
# adverbs


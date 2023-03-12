from dataclasses import dataclass
from enum import Enum
from POS import POS
from POS import Word
from POS import Sentence
from POS import Phrase
from POS import RELATION
from PreprocessingDict import PreprocessingDict
from datetime import datetime
from typing import List
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
        # try:
            print(f"sentence: '{sentence}'")
            print(f"question: '{question}'")
            formattedSentence = self.parseSentence(sentenceRaw=sentence)
            formattedQuestion = self.parseSentence(sentenceRaw=question.replace("?",""))

            for questionWord in self.THE_FIVE_WS:
                if questionWord in question.lower():
                    i = [x for x in formattedQuestion.words if x.text == questionWord]
                    # secondaryWord = formattedQuestion.words[i+1]
                    secondaryWord = formattedQuestion.verbPhrase.text
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
        # except:
        #     return None


    def parseSentence(self, sentenceRaw):
        wordStrings = sentenceRaw.replace('.','').split()
        words = []
        for string in wordStrings:
            try:
                word = self.wordDict[string.lower()]
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

        phrases = []
        # Find the subject
        i = 0
        wordsInPhrase = []
        for i in range(i, len(words)):
            word = words[i]
            if not IsWordAnyPos(word, {POS.VERB, POS.ADV}):
                wordsInPhrase.append(word)
            else:
                newPhrase = Phrase(
                    text = " ".join(word.text for word in wordsInPhrase),
                    words = wordsInPhrase,
                    relation = RELATION.SUBJECT
                )
                phrases.append(newPhrase)
                break

        # Find the verb  
        wordsInPhrase = []
        for i in range(i, len(words)):
            word = words[i]
            if IsWordAnyPos(word, {POS.VERB, POS.ADV}):
                wordsInPhrase.append(word)
            else:
                newPhrase = Phrase(
                    text = " ".join(word.text for word in wordsInPhrase),
                    words = wordsInPhrase,
                    relation = RELATION.VERB
                )
                phrases.append(newPhrase)
                break
        
        # Find the Indirect Object, if any
        if IsWordAnyPos(word, {POS.PRON, POS.PROPN}): 
            wordsInPhrase = []
            for i in range(i, len(words)):
                word = words[i]
                if IsWordAnyPos(word, {POS.PRON, POS.PROPN, POS.NOUN}):
                    wordsInPhrase.append(word)
                else:
                    newPhrase = Phrase(
                        text = " ".join(word.text for word in wordsInPhrase),
                        words = wordsInPhrase,
                        relation = RELATION.INDIRECTOBJ
                    )
                    phrases.append(newPhrase)
                    break
                    
        # Find the Direct Object, if any
        if not IsWordAnyPos(word, {POS.ADP}) and IsWordAnyPos(word, {POS.NOUN, POS.ADJ, POS.NUM}):
            wordsInPhrase = []
            for i in range(i, len(words)):
                word = words[i]
                if not IsWordAnyPos(word, {POS.ADP}):
                    wordsInPhrase.append(word)
                else:
                    newPhrase = Phrase(
                        text = " ".join(word.text for word in wordsInPhrase),
                        words = wordsInPhrase,
                        relation = RELATION.DIRECTOBJ
                    )
                    phrases.append(newPhrase)
                    break

        # Find all propositional & other phrases
        
        while i < len(words):
            wordsInPhrase = []
            for i in range(i, len(words)):
                word = words[i]
                if len(wordsInPhrase) > 0 and (IsWordAnyPos(word, {POS.ADP, POS.SCONJ}) or word.text == "every"):
                    i = i - 1
                    break
                else:
                    wordsInPhrase.append(word)
            newPhrase = Phrase(
                text = " ".join(word.text for word in wordsInPhrase),
                words = wordsInPhrase,
                relation = RELATION.PREP
            )
            phrases.append(newPhrase)
            i = i + 1

        mentionsTime = "time" in sentenceRaw.lower()

        nonStopWords = list(filter(lambda word: not word.isStop, words))

        sentence = Sentence(
            text = sentenceRaw,
            words = words,
            phrases = phrases,
            subjectPhrase = phrases[0],
            verbPhrase = phrases[1],
            nonStopWords = nonStopWords,
            mentionsTime = mentionsTime
        )
        return sentence

    def Find_Who(self, sentence:Sentence, question:Sentence):
        # looking for a propernoun, pronoun, or even noun when combined with a pronoun
        if "with" in sentence.text:
            containingPhrase = list(filter(lambda phrase: "with" in phrase.text, sentence.phrases))[0]
            answer = containingPhrase.text.replace("with","").strip()

            # for phrase in sentence.phrases
        
        elif question.words[-1].text == "with":
            names = []
            # propernounsInQuestion = list(filter(lambda word: any(pos.value in {POS.PROPN.value, POS.PRON.value, POS.NOUN.value} for pos in word.posList), question.words))
            nounsInQuestion = GetWordsOfPos(question.words, {POS.PROPN, POS.PRON, POS.NOUN})
            for person in sentence.subjectPhrase.words:
                if IsWordAnyPos(person, {POS.PROPN, POS.PRON, POS.NOUN}) and person not in nounsInQuestion:
                    names.append(person.text)
            answer = " and ".join(names)
            # list(filter(lambda word: any(name in question.subject for name in sentence.subject), sentence.subject))[0]
            # answer = any(name not in sentence.subject for name in question.subject).text  
        else:
            names = []
            for person in sentence.subjectPhrase.words:
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
        indirectObjectList = list(filter(lambda phrase: phrase.relation.value == RELATION.INDIRECTOBJ.value, sentence.phrases))
        if len(indirectObjectList) > 0:
            indirectObject:Phrase = indirectObjectList[0]
            names = []
            for person in indirectObject.words:
                if IsWordAnyPos(person, {POS.PROPN, POS.PRON, POS.NOUN}):
                    names.append(person.text)
            answer = " and ".join(names)
            return answer

        # prepPhraseList = list(filter(lambda phrase: phrase.relation.value == RELATION.PREP.value and (IsWordAnyPos(word, {POS.PROPN, POS.PRON, POS.NOUN}) for word in phrase.words), sentence.phrases))
        prepPhraseList = list(filter(lambda phrase: phrase.relation.value == RELATION.PREP.value and "to" in phrase.text, sentence.phrases))

        if len(prepPhraseList) > 0:
            prepPhrase:Phrase = prepPhraseList[0]
            names = []
            for person in prepPhrase.words:
                if IsWordAnyPos(person, {POS.PROPN, POS.PRON, POS.NOUN}):
                    names.append(person.text)
            answer = " and ".join(names)
            return answer
        # for person in sentence.indirectObject:
        #     if any(pos.value in {POS.PROPN.value} for pos in person.posList):
        #         names.append(person.text)
        # answer = " and ".join(names)
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
        if IsWordAnyPos(question.words[1], {POS.ADJ}):
            obj = question.indirectObject[0]

        # if POS.ADJ in question.words[1].pos:
            # obj = question.directObject[0]
            i = sentence.words.index(obj)
            if IsWordAnyPos(sentence.words[i-1], {POS.ADJ}):
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

def IsWordAnyPos(word: Word, posList:list ):
    newList = []
    for pos in posList:
        newList.append(pos.value)
    return any(pos.value in newList for pos in word.posList)

def GetWordsOfPos(words: List[Word], lst:list ):
    return list(filter(lambda word: IsWordAnyPos(word, lst), words))

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


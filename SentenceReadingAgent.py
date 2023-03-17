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
import time
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
        tic = time.perf_counter()
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
                    # i = [x for x in formattedQuestion.words if x.text == questionWord]
                    # secondaryWord = formattedQuestion.words[i+1]
                    # secondaryWord = formattedQuestion.verbPhrase.text
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

            toc = time.perf_counter()
            print(f"{toc - tic:0.6f} seconds")
            return answer
        except:
            return None


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

        uncheckedWords = words.copy()
        i = 0
        phrases = []
        subjectPhrase = None
        verbPhrase = None
        directObjPhrase = None
        indirectObjPhrase = None

        while len(uncheckedWords) > 0:
            word = uncheckedWords[0]
            wordsInPhrase = [word]
            # uncheckedWords.remove(word)
            relation = None

            # If there is a demonstrative, such as "this year". Form of DEMON ... NOUN
            if IsWordAnyPos(word, {POS.DEMON}):
                relation = RELATION.PREP
                for i in range(1, len(uncheckedWords)):
                    word = uncheckedWords[i]
                    if IsWordAnyPos(word, {POS.PRON, POS.PROPN, POS.NOUN, POS.ADJ, POS.CCONJ}) :
                        wordsInPhrase.append(word)
                    else:
                        break
            # subject
            elif IsWordAnyPos(word, {POS.ADJ, POS.NOUN, POS.PRON, POS.PROPN, POS.NUM, POS.ART, POS.CCONJ}) and subjectPhrase is None and verbPhrase is None:
                relation = RELATION.SUBJECT
                for i in range(1, len(uncheckedWords)):
                    word = uncheckedWords[i]
                    if IsWordAnyPos(word, {POS.ADJ, POS.NOUN, POS.PRON, POS.PROPN, POS.NUM, POS.ART, POS.CCONJ}) or word.text == "of":
                        wordsInPhrase.append(word)
                    else:
                        break
            # Primary verb
            elif IsWordAnyPos(word, {POS.VERB, POS.ADV}) and verbPhrase is None:
                relation = RELATION.VERB
                for i in range(1, len(uncheckedWords)):
                    word = uncheckedWords[i]
                    if IsWordAnyPos(word, {POS.VERB, POS.ADV, POS.AUX}) :
                        wordsInPhrase.append(word)
                    else:
                        break

            # indirect object
            elif not IsWordAnyPos(word, {POS.ADP, POS.DEMON}) and IsWordAnyPos(word, {POS.PRON, POS.PROPN}) and indirectObjPhrase is None and verbPhrase is not None:
                relation = RELATION.INDIRECTOBJ
                for i in range(1, len(uncheckedWords)):
                    word = uncheckedWords[i]
                    if IsWordAnyPos(word, {POS.PRON, POS.PROPN, POS.NOUN}) and word.text != "all":
                        wordsInPhrase.append(word)
                    else:
                        break
            # direct object
            elif not IsWordAnyPos(word, {POS.ADP, POS.DEMON}) and IsWordAnyPos(word, {POS.PRON, POS.PROPN, POS.NOUN, POS.ADJ, POS.NUM, POS.ART}) and directObjPhrase is None and verbPhrase is not None:
                relation = RELATION.DIRECTOBJ
                for i in range(1, len(uncheckedWords)):
                    word = uncheckedWords[i]
                    if not IsWordAnyPos(word, {POS.ADP, POS.DEMON}):# and not (IsWordAnyPos(word, {POS.ADJ}) and IsWordAnyPos(uncheckedWords[i+1], {POS.PRON, POS.PROPN, POS.NOUN})):
                        wordsInPhrase.append(word)
                    else:
                        break
            # prepositional phrase
            else:
                relation = RELATION.PREP
                for i in range(1, len(uncheckedWords)):
                    word = uncheckedWords[i]
                    if len(wordsInPhrase) > 0 and (IsWordAnyPos(word, {POS.ADP, POS.SCONJ, POS.DEMON}) or word.text == "every"):
                        break
                    else:
                        wordsInPhrase.append(word)
            for word in wordsInPhrase:
                uncheckedWords.remove(word)
            newPhrase = Phrase(
                text = " ".join(word.text for word in wordsInPhrase),
                words = wordsInPhrase,
                relation = relation
            )
            phrases.append(newPhrase)
            if relation == RELATION.VERB:
                verbPhrase = newPhrase
            elif relation == RELATION.SUBJECT:
                subjectPhrase = newPhrase
            elif relation == RELATION.INDIRECTOBJ:
                indirectObjPhrase = newPhrase
            elif relation == RELATION.DIRECTOBJ:
                directObjPhrase = newPhrase


        mentionsTime = "time" in sentenceRaw.lower()

        nonStopWords = list(filter(lambda word: not word.isStop, words))

        sentence = Sentence(
            text = sentenceRaw,
            words = words,
            phrases = phrases,
            subjectPhrase = subjectPhrase,
            verbPhrase = verbPhrase,
            indirectObjPhrase = indirectObjPhrase,
            directObjPhrase = directObjPhrase,
            nonStopWords = nonStopWords,
            mentionsTime = mentionsTime
        )
        return sentence

    def Find_Who(self, sentence:Sentence, question:Sentence):
        # looking for a propernoun, pronoun, or even noun when combined with a pronoun
        if "with" in sentence.text:
            containingPhrase = list(filter(lambda phrase: "with" in phrase.text, sentence.phrases))[0]
            answer = containingPhrase.text.replace("with","").strip()
        elif "with" in question.text:
            names = []
            nouns = GetWordsOfPos(question.words, {POS.PROPN, POS.PRON, POS.NOUN})
            for person in sentence.subjectPhrase.words:
                if IsWordAnyPos(person, {POS.PROPN, POS.PRON, POS.NOUN}) and person not in nouns:
                    names.append(person.text)
            if "and" in sentence.subjectPhrase.text:
                answer = " and ".join(names)
            else:
                answer = " ".join(names)
        elif question.words[1].text == "was" and IsWordAnyPos(question.words[2], {POS.VERB}):
            names = []
            nouns = GetWordsOfPos(sentence.indirectObjPhrase.words, {POS.PROPN, POS.PRON, POS.NOUN})
            for person in sentence.indirectObjPhrase.words:
                if IsWordAnyPos(person, {POS.PROPN, POS.PRON, POS.NOUN}):
                    names.append(person.text)
            if "and" in sentence.indirectObjPhrase.text:
                answer = " and ".join(names)
            else:
                answer = " ".join(names)
        else:
            names = []
            if sentence.subjectPhrase != None:
                for person in sentence.subjectPhrase.words:
                    if IsWordAnyPos(person, {POS.PROPN, }):
                        names.append(person.text)
                if len(names) == 0:
                    for person in sentence.subjectPhrase.words:
                        if IsWordAnyPos(person, {POS.NOUN}):
                            names.append(person.text)
                if len(names) == 0:
                    for person in sentence.subjectPhrase.words:
                        if IsWordAnyPos(person, {POS.PRON}):
                            names.append(person.text)

            elif sentence.directObjPhrase != None:
                for person in sentence.directObjPhrase.words:
                    if IsWordAnyPos(person, {POS.PROPN, }):
                        names.append(person.text)
                if len(names) == 0:
                    for person in sentence.directObjPhrase.words:
                        if IsWordAnyPos(person, {POS.NOUN}):
                            names.append(person.text)
                if len(names) == 0:
                    for person in sentence.directObjPhrase.words:
                        if IsWordAnyPos(person, {POS.PRON}):
                            names.append(person.text)
                # for person in sentence.directObjPhrase.words:
                #     if IsWordAnyPos(person, {POS.PROPN, POS.PRON, POS.NOUN}):
                #         names.append(person.text)
            answer = " ".join(names)

        return answer

    def Find_Whom(self, sentence:Sentence, question:Sentence):
        names = []
        indirectObjectList = list(filter(lambda phrase: phrase.relation.value == RELATION.INDIRECTOBJ.value, sentence.phrases))
        if len(indirectObjectList) > 0:
            indirectObject:Phrase = indirectObjectList[0]
            names = []
            for person in indirectObject.words:
                if IsWordAnyPos(person, {POS.PROPN, POS.PRON, POS.NOUN}):
                    names.append(person.text)
            answer = " and ".join(names)
            return answer

        prepPhraseList = list(filter(lambda phrase: phrase.relation.value == RELATION.PREP.value and "to" in phrase.text, sentence.phrases))

        if len(prepPhraseList) > 0:
            prepPhrase:Phrase = prepPhraseList[0]
            names = []
            for person in prepPhrase.words:
                if IsWordAnyPos(person, {POS.PROPN, POS.PRON, POS.NOUN}):
                    names.append(person.text)
            answer = " and ".join(names)
            return answer
        return answer

    def Find_What(self, sentence:Sentence, question:Sentence):
        dobjPhraseList = list(filter(lambda phrase: phrase.relation.value == RELATION.DIRECTOBJ.value, sentence.phrases))
        if question.words[1].text in {"did", "will"} and len(dobjPhraseList) > 0:
            prepPhrase:Phrase = dobjPhraseList[0]
            whats = []
            for person in prepPhrase.words:
                if IsWordAnyPos(person, {POS.PROPN, POS.PRON, POS.NOUN}):
                    whats.append(person.text)
            answer = " and ".join(whats)
            if len(whats) == 0:
                answer = prepPhrase.text

            return answer
        elif question.words[1].text in {"is","was"}:
            if question.directObjPhrase is not None and len(question.directObjPhrase.words) > 0:
                adjPhraseList = list(filter(lambda phrase: question.directObjPhrase.words[0] in phrase.words, sentence.phrases))
                if len(adjPhraseList) > 0:
                    nouns = list(filter(lambda word: IsWordAnyPos(word, {POS.NOUN}), adjPhraseList[0].words))
                    if len(nouns) > 0:
                        return nouns[0].text

            elif sentence.subjectPhrase is not None:

            
            

            # prepPhrase = question.words.index
            # prepPhrase:Phrase = prepPhraseList[0]
                return sentence.subjectPhrase.text
            # return sentence.directObject[0].text
        # elif question.words[1].text == "will" and len(phraseList) > 0:
        #     # find verb
        #     verbPhrase =
        #     pass
        elif question.words[1].text in {"do"}:
            verb = [word for word in sentence.verbPhrase.words if IsWordAnyPos(word, {POS.VERB})][0]
            return verb.text
        # elif sentence.directObjPhrase != None:

        #     return
        else:
            return self.Find_Who(sentence, question)
        pass

    def Find_When(self, sentence:Sentence, question:Sentence):
        for phrase in sentence.phrases:
            if len(GetWordsOfPos(phrase.words, {POS.DEMON})) > 0:
                return phrase.text

        # demonstrativePhraseList = list(filter(lambda phrase: any(word for word in phrase.words if IsWordAnyPos(word, {POS.DEMON}),phrase), sentence.phrases))
        time = [word for word in sentence.words for pos in word.posList if pos.value == POS.TIME.value]
        if len(time) > 0:
            # [0]
            # time = [word for word in sentence.words if POS.TIME in word.posList][0]
            return time[0].text
        # elif

    def Find_Where(self, sentence:Sentence, question:Sentence):
        # pay attention to "to" and "from"
        for phrase in list(filter(lambda phrase: phrase.relation.value == RELATION.PREP.value and any(w in phrase.text for w in {"to","from"}), sentence.phrases)):
            nouns = list(filter(lambda word: IsWordAnyPos(word, {POS.NOUN}), phrase.words))
            if len(nouns) > 0:
                noun = nouns[0]
                return noun.text

        # # I need to find "to <noun>"
        # indices = [i for i in range(len(sentence.words)) if sentence.words[i].text == "to"]
        # # i = sentence.words.index(self.wordDict["to"])
        # for i in indices:
        #     for j in range(i, len(sentence.words)):
        #         nextWord = sentence.words[j]
        #         if any(pos.value in {POS.NOUN.value} for pos in nextWord.posList):
        #             return nextWord.text
        #         elif any(pos.value in {POS.VERB.value} for pos in nextWord.posList):
        #             break

        #  # I need to find "from ... <noun>"
        # indices = [i for i in range(len(sentence.words)) if sentence.words[i].text == "from"]
        # # i = sentence.words.index(self.wordDict["to"])
        # for i in indices:
        #     for j in range(i, len(sentence.words)):
        #         nextWord = sentence.words[j]
        #         if any(pos.value in {POS.NOUN.value} for pos in nextWord.posList):
        #             return nextWord.text
        #         elif any(pos.value in {POS.VERB.value} for pos in nextWord.posList):
        #             break
        return None

    def Find_Why(self, sentence:Sentence, question:Sentence):
        pass

    def Find_How(self, sentence:Sentence, question:Sentence):

        # if any(pos.value in {POS.ADJ.value} for pos in sentence.words[1].posList):
        if IsWordAnyPos(question.words[1], {POS.ADJ}):
            # locate noun associated with adjective
            nounInQuestion = list(filter(lambda word: IsWordAnyPos(word, {POS.PROPN, POS.PRON, POS.NOUN}), question.words))
            phraseList = list(filter(lambda phrase: nounInQuestion[0].text in phrase.text, sentence.phrases))
            if len(phraseList) > 0:
                adjectives = GetWordsOfPos(phraseList[0].words, {POS.ADJ})
                return adjectives[0].text
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
            phrase = list(filter(lambda phrase: phrase.relation == RELATION.VERB, sentence.phrases))[0]
            primaryVerb = list(filter(lambda word: IsWordAnyPos(word, {POS.VERB}), phrase.words))[0]
            return primaryVerb.text
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


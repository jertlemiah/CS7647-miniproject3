from SentenceReadingAgent import SentenceReadingAgent

def test():
    #This will test your SentenceReadingAgent
	#with nine initial test cases.

    test_agent = SentenceReadingAgent()

    sentence_1 = "Ada brought a short note to Irene."
    question_1 = "Who brought the note?"
    question_2 = "What did Ada bring?"
    question_3 = "Who did Ada bring the note to?"
    question_4 = "How long was the note?"

    sentence_2 = "David and Lucy walk one mile to go to school every day at 8:00AM when there is no snow."
    question_5 = "Who does Lucy go to school with?"
    question_6 = "Where do David and Lucy go?"
    question_7 = "How far do David and Lucy walk?"
    question_8 = "How do David and Lucy get to school?"
    question_9 = "At what time do David and Lucy walk to school?"

    sentence_3 = "Frank took the horse to the farm."
    question_10 = "Where did the horse go?"
    
    sentence_4 = "She told her friend a story."
    question_4_1 = "What did she tell?"
    question_4_2 = "Who told a story?"

    sentence_5 = "The house is made of paper."
    question_5_1 = "What is made of paper?"

    sentence_6 = "This tree came from the island."
    question_6_1 = "Where did the tree come from?"

    sentence_7 = "Serena saw a home last night with her friend."
    question_7_1 = "Who was with Serena?"

    # Who / whom questions
    # print(test_agent.solve(sentence_1, question_1))  # "Ada"
    # print(test_agent.solve(sentence_1, question_3))  # "Irene"
    print(test_agent.solve(sentence_2, question_5))  # "David"
    # print(test_agent.solve(sentence_4, question_4_2))  # "She"
    # print(test_agent.solve(sentence_7, question_7_1))  # her friend

    # What questions
    # print(test_agent.solve(sentence_1, question_2))  # "note" or "a note"
    # print(test_agent.solve(sentence_2, question_9))  # "8:00AM"
    # print(test_agent.solve(sentence_4, question_4_1))  # a story
    # print(test_agent.solve(sentence_5, question_5_1))  # the house

    # When questions

    # How questions
    # print(test_agent.solve(sentence_1, question_4))  # "short"
    # print(test_agent.solve(sentence_2, question_7))  # "mile"
    # print(test_agent.solve(sentence_2, question_8))  # "walk"

    # Where questions
    # print(test_agent.solve(sentence_2, question_6))  # "school"
    # print(test_agent.solve(sentence_3, question_10))  # "farm"
    # print(test_agent.solve(sentence_6, question_6_1))  # "island"
    

if __name__ == "__main__":
    test()
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
    question_4_3 = "Who was told a story?"

    sentence_5 = "The house is made of paper."
    question_5_1 = "What is made of paper?"

    sentence_6 = "This tree came from the island."
    question_6_1 = "Where did the tree come from?"

    sentence_7 = "Serena saw a home last night with her friend."
    question_7_1 = "Who was with Serena?"

    sentence_8 = "This year David will watch a play."
    question_8_1 = "What will David watch?"

    sentence_9 = "The water is blue."
    question_9_1 = "What is blue?"

    sentence_10 = "The white dog and the blue horse play together."
    question_10_1 = "What do the dog and horse do?"

    sentence_11 = "Serena and Ada took the blue rock to the street."
    question_11_1 = "Where did they take the rock?"
    question_11_2 = "Who was with Ada?"
    question_11_3 = "What was blue?"

    sentence_12 = "Bring the dog to the other room."
    question_12_1 = "What should be brought to the other room?"
    
    sentence_13 = "Lucy will write a book."
    question_13_1 = "Who will write a book?"
    
    sentence_14 = "Serena ran a mile this morning."
    question_14_1 = "When did Serena run?"

    sentence_15 = "Give us all your money."
    question_15_1 = "What should you give us?"

    sentence_16 = "The sound of rain is cool."
    question_16_1 = "What is cool?"

    sentence_17 = "Their children are in school."
    question_17_1 = "Who is in school?"

    # Who / whom questions
    print(test_agent.solve(sentence_1, question_1))  # "Ada"
    print(test_agent.solve(sentence_1, question_3))  # "Irene"
    print(test_agent.solve(sentence_2, question_5))  # "David"
    print(test_agent.solve(sentence_4, question_4_2))  # "She"
    print(test_agent.solve(sentence_4, question_4_3))  # "her friend"
    print(test_agent.solve(sentence_7, question_7_1))  # her friend
    print(test_agent.solve(sentence_11, question_11_2))  # Serena
    print(test_agent.solve(sentence_17, question_17_1))  # their children

    # What questions
    print(test_agent.solve(sentence_1, question_2))  # "note" or "a note"
    print(test_agent.solve(sentence_2, question_9))  # "8:00AM"
    print(test_agent.solve(sentence_4, question_4_1))  # a story
    print(test_agent.solve(sentence_5, question_5_1))  # the house
    print(test_agent.solve(sentence_8, question_8_1))  # a play
    print(test_agent.solve(sentence_9, question_9_1))  # the water
    print(test_agent.solve(sentence_10, question_10_1))  # play
    print(test_agent.solve(sentence_12, question_12_1))  # the dog
    print(test_agent.solve(sentence_15, question_15_1))  # money
    print(test_agent.solve(sentence_16, question_16_1))  # the sound of rain
    print(test_agent.solve(sentence_11, question_11_3))  # the rock


    # When questions
    print(test_agent.solve(sentence_14, question_14_1))  # this morning

    # How questions
    print(test_agent.solve(sentence_1, question_4))  # "short"
    print(test_agent.solve(sentence_2, question_7))  # "mile"
    print(test_agent.solve(sentence_2, question_8))  # "walk"

    # # Where questions
    print(test_agent.solve(sentence_2, question_6))  # "school"
    print(test_agent.solve(sentence_3, question_10))  # "farm"
    print(test_agent.solve(sentence_6, question_6_1))  # "island"
    print(test_agent.solve(sentence_11, question_11_1))  # "island"
    

if __name__ == "__main__":
    test()
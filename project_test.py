# English level test - read questions from text file

import sys
import pickle, shelve

records = {}

def open_file(file_name, mode):
    """Open up the file"""
    try:
        the_file = open(file_name, mode)
    except IOError as e:
        print("the file can't be open", file_name, "the program will be finished\n", e)
        sys.exit()
    else:
        return the_file

def next_line(the_file):
    """returns formatted further line of test file"""
    line = the_file.readline()
    line = line.replace("/", "\n")
    return line

def next_block(the_file):
    """Returns next block of test file"""
    category = next_line(the_file)

    question = next_line(the_file)

    answers = []
    for i in range(4):
        answers.append(next_line(the_file))

    correct = next_line(the_file)
    if correct:
        correct = correct[0]

    explanation = next_line(the_file)

    return category, question, answers, correct, explanation

def welcome(title, name):
    """Greet the user"""
    print(name,"\t\t, You are welcome to complete\n")
    print("\t\t", title, "\n")

def level(score):
    """define level of english"""
    user_level = ""
    if score < 20:
        user_level = "elementary"
    elif score < 30:
        user_level = "intermediate"
    elif score < 35:
        user_level = "upper intermediate"
    else:
        user_level = "advanced"
    return user_level

def main():
    test_file = open_file("test.txt", "r")
    name = input("Enter user name:\t")
    title = next_line(test_file)
    welcome(title, name)
    score = 0

    # extract the first block
    category, question, answers, correct, explanation = next_block(test_file)
    while category:
        # output the question to the screen
        print(category)
        print(question)
        for i in range(4):
            print("\t", i + 1, "-", answers[i])

        # get the answer
        answer = input("Your answer: ")

        # check the answer
        if answer == correct:
            print("\ncorrect")
            score += 1
        else:
            print("\nwrong", end=" ")
            print(explanation)
        print("Correct answers:", score, "\n\n")

        # переход к следующему вопросу
        category, question, answers, correct, explanation = next_block(test_file)

    test_file.close()
    result = level(score)
    print("The last question has been completed")
    print("Correct answers: ", score)
    print(f"Your English level proficiency is {result}")

if __name__ == '__main__':
    main()
"""
<тема вопроса>
<вопрос>
<ответ 1>
<ответ 2>
<ответ З>
<ответ 4>
<правильный ответ>
<комментарий>
"""
import os
import smtplib, csv, sys
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)

# Registrants
students = []
answer = ''
score = 0


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def get_register():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    age = request.form.get("age")
    email = request.form.get("email")
    if not name or not email or not age:
        return render_template("failure.html")
    message = "You are registered for English level test!"
    return render_template("success.html", message=message)
    # return jsonify(name, age, email, message)

@app.route("/update", methods=["POST"])
def update():
    for item in request.form:
        session[item] = int(request.form.get(item))
    return redirect("/test")

@app.route("/test")
def get_test():
    data = {}
    test_file = open_file("test.txt", "r")
    title = next_line(test_file)



    # extract the first block
    category, question, answers, correct, explanation = next_block(test_file)

    while category:
        # get the answer
        # answer = request.form.get("answer")
        message = ''

        # check the answer
        if answer == correct:
            message = 'Correct'
            score += 1
        else:
            message = 'Wrong: ' + explanation

        # переход к следующему вопросу
        category, question, answers, correct, explanation = next_block(test_file)
        # arrCategory.append()

        return render_template("test.html", category=category,
            question=question, answers=answers,
            correct=correct, explanation=explanation, message=message)

    test_file.close()

@app.route("/test", methods=["POST"])
def post_test():
    answer = request.form.get("answer")
    return redirect('test')



# @app.route("/test")
# def get_test():
    # return render_template("test.html")

@app.route("/test_old")
def test():
    test_file = open_file("test.txt", "r")
    title = next_line(test_file)

    score = 0

    # extract the first block
    # category, question, answers, correct, explanation = next_block(test_file)



    while category:
        # output the question to the screen
        # print(category)
    #     print(question)
        # for i in range(4):
    #         print("\t", i + 1, "-", answers[i])

        # get the answer
        answer = request.form.get("answer")
        message = ''
        # check the answer
        if answer == correct:
            message = 'Correct'
    #         print("\ncorrect")
            score += 1
        else:
            message = 'Wrong: ' + explanation
    #         print("\nwrong", end=" ")
    #         print(explanation)
    #     print("Correct answers:", score, "\n\n")

        # переход к следующему вопросу
        category, question, answers, correct, explanation = next_block(test_file)

    test_file.close()
    result = level(score)
    # print("The last question has been completed")
    # print("Correct answers: ", score)
    # print(f"Your English level proficiency is {result}")
    return jsonify({"result": result, "message": message})

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


    # return {"category": category, "question": question, "question": answers, "correct": correct, "explanation": explanation}
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

#def main():



"""Create a file with results of users
    file = open("registrants.csv", "a")
    writer = csv.writer(file)
    writer.writerow((name, age, result))
    file.close()
    """
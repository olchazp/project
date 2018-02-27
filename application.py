import os
import smtplib, csv, sys
from flask import Flask, render_template, request, jsonify, redirect, session

app = Flask(__name__)

# Variables
answer = ''
score = 0
questions =[]
grade = ""
number = 0

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

@app.route("/test")
def get_test():
    test_file = open_file("test.txt", "r")
    title = next_line(test_file)
    # extract blocks from file
    for i in range (40):
        questions.append(next_block(test_file))
    test_file.close()
    return render_template("test.html", questions = questions)

@app.route("/test", methods=["POST"])
def update():
    for item in questions:
        item["answer"] = request.form.get("answer")
        if item["answer"] == item["correct"]:
            grade = "Correct"
            score += 1
        else:
            grade = 'Wrong: ' + item["explanation"]
        item["mark"] = grade

    return render_template("test_check.html", questions = questions)



@app.route("/results")
def get_results():
    result = level(score)
    return render_template("results.html", result = result, score = score)

    #return jsonify({"result": result, "message": message})


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
    item = {}
    item["category"] = next_line(the_file)

    item["question"] = next_line(the_file)

    item["answers"] = []
    for i in range(4):
        item["answers"].append(next_line(the_file))

    item["correct"] = next_line(the_file)
    if item["correct"]:
        item["correct"] = item["correct"][0]

    item["explanation"] = next_line(the_file)
    return item


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


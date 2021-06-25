import numpy as np
from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        req = request.get_json(force=True)
        # req = {"list": [0, 4, 7, 8]}

        data = getJsonData('db.json')

        matrix = data["matrix"]
        courses = data["courses"]
        n = len(matrix)

        answers = [0] * n
        for i in req["list"]: answers[i] = 1

        res = np.dot(np.array(answers).reshape(1, n), matrix)[0]
        ind = np.argpartition(res, -5)[-5:]

        result = {}
        sum = np.sum(res[ind])
        for i in ind: result[courses[i]] = res[i] / sum

        return json.JSONEncoder().encode(result)

    else:
        data = getJsonData('db.json')
        quizStructure = data["quiz"]
        questionsList = data["text"]
        matrix = data["matrix"]

        result = {
            "quiz": [],
            "matrix": matrix
        }
        for quizQuestion in quizStructure:
            result["quiz"].append({})
            for quizQuestionItem in quizQuestion:
                result["quiz"][-1][quizQuestionItem] = questionsList[int(quizQuestionItem)]

        return json.JSONEncoder().encode(result)


@app.route('/v2', methods=['POST', 'GET'])
def v2():
    data = getJsonData('db.json')
    quizStructure = data["quiz"]
    questionsList = data["text"]
    matrix = data["matrix"]
    prof_coeffs = data["prof_coeffs"]

    result = {
        "quiz": [],
        "matrix": matrix,
        "prof_coeffs": prof_coeffs
    }
    for quizQuestion in quizStructure:
        result["quiz"].append({})
        for quizQuestionItem in quizQuestion:
            result["quiz"][-1][quizQuestionItem] = questionsList[int(quizQuestionItem)]

    return json.JSONEncoder().encode(result)


@app.route('/directions', methods=['GET'])
def directions():
    return json.JSONEncoder().encode(getJsonData("directions.json"))


@app.route('/professions', methods=['GET'])
def professions():
    return json.JSONEncoder().encode(getJsonData("professions.json"))


def getJsonData(path):
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)

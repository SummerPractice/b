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

        print(result)

        return json.JSONEncoder().encode(result)

    else:
        data = getJsonData('db.json')
        quizStructure = data["quiz"]
        questionsList = data["text"]

        result = []
        for quizQuestion in quizStructure:
            result.append({})
            for quizQuestionItem in quizQuestion:
                result[-1][quizQuestionItem] = questionsList[int(quizQuestionItem)]

        print(result)

        return json.JSONEncoder().encode(result)


def getJsonData(path):
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)

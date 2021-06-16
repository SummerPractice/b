import numpy as np
from flask import Flask, request
import xlwings as xw
import json

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # print(request.data)
        # print(request.json)
        # print(request.get_json(force=True))

        req = request.get_json(force=True)
        print(req)

        book = xw.Book('db.xlsx')
        sheet = book.sheets['k']
        n = int(sheet.range("L1").value)

        matrix = np.array(list(map(
            lambda e: e.value if e.value else 0,
            sheet.range((2, 2), (n + 1, 11))
        ))).reshape(n, 10)

        answers = [0] * n
        for i in req["list"]: answers[i] = 1

        res = np.dot(np.array(answers).reshape(1, n), matrix)[0]
        ind = np.argpartition(res, -5)[-5:]
        couses = ["270302", "270304", "270305", "090301", "090303", "090304", "270303", "090302", "020302", "020303"]
        result = {}
        sum = np.sum(res[ind])
        print(res[ind])
        print(sum)
        for i in ind: result[couses[i]] = res[i] / sum

        return json.JSONEncoder().encode(result)

    else:
        book = xw.Book('db.xlsx')
        quiz = book.sheets['quiz']
        quizQuestionCount = quiz.range("C1").value
        quizStructure = list(map(lambda e: e.value, quiz.range((1, 2), (quizQuestionCount, 2))))
        quizStructure = list(map(lambda e: list(e.strip().split(";")), quizStructure))

        questionsSheet = book.sheets['questions']
        questionsCount = questionsSheet.range("C1").value
        questionsList = list(map(
            lambda e: e.value,
            questionsSheet.range((1, 2), (questionsCount, 2))
        ))

        result = []
        for quizQuestion in quizStructure:
            result.append({})
            for quizQuestionItem in quizQuestion:
                result[-1][quizQuestionItem] = questionsList[int(quizQuestionItem)]

        return json.JSONEncoder().encode(result)

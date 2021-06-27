import numpy as np
import pymysql
from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/users', methods=['POST'])
def users():

    req = request.get_json(force=True)

    try:
        connection = pymysql.connect(
            host="eu-cdbr-west-01.cleardb.com",
            port=3306,
            user="b4a5dd03d2964c",
            password="9246ee1e",
            database="heroku_65d7e04abe36d4e",
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO `user` (first_name, last_name, email, math, rus, phys, inf, individual) VALUES " \
                               "('%s', '%s', '%s', %i, %i, %i, %i, %i);" % (
                                   req["firstname"], req["lastname"], req["email"],
                                   req["math"], req["rus"], req["phys"], req["inf"],
                                   req["individual"])
                cursor.execute(insert_query)

            connection.commit()

        finally:
            connection.close()

    except Exception as e:
        print(e)

    return "All good"

@app.route('/questions', methods=['GET'])
def questions():
    data = getJsonData('db.json')
    quizStructure = data["quiz"]
    questionsList = data["text"]
    matrix = data["matrix"]
    prof_coeffs = data["prof"]

    result = {
        "quiz": [],
        "matrix": matrix,
        "prof": prof_coeffs
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

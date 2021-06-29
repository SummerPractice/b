import pymysql
from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/users', methods=['POST'])
def users():
    req = request.get_json(force=True)
    insert_query = "INSERT INTO `user` (first_name, last_name, email, math, rus, phys, inf, individual) VALUES " \
                   "('%s', '%s', '%s', %i, %i, %i, %i, %i);" % (
                       req["firstname"], req["lastname"], req["email"],
                       req["math"], req["rus"], req["phys"], req["inf"],
                       req["individual"])

    dbFetch(insert_query)
    return "All good"


@app.route('/questions', methods=['GET'])
def questions():
    data = dbFetch("SELECT * FROM answer WHERE question_id IS NOT NULL ORDER BY question_id")
    questionsCount = data[-1]['question_id'] + 1
    answersCount = len(data)

    quiz = []
    matrix = [[] for x in range(answersCount)]
    prof = [None for x in range(answersCount)]

    for i in range(questionsCount):
        question = {}
        question_answers = [x for x in data if x['question_id'] == i]
        for answer in question_answers:
            question[answer['answer_id']] = answer['text']
        quiz.append(question)

    for i in range(answersCount):
        answer_id = data[i]["answer_id"]

        matrix[answer_id] = [
            data[i]["270302"],
            data[i]["270304"],
            data[i]["270305"],
            data[i]["090301"],
            data[i]["090303"],
            data[i]["090304"],
            data[i]["270303"],
            data[i]["090302"],
            data[i]["020302"],
            data[i]["020303"]
        ]

        prof[answer_id] = data[i]["prof_id"]

    result = {
        "quiz": quiz,
        "matrix": matrix,
        "prof": prof
    }

    return json.JSONEncoder().encode(result)


@app.route('/directions', methods=['GET'])
def directions():
    data = dbFetch("SELECT * FROM direction")

    result = []
    for i in data:
        result.append({
            "id": i["id"],
            "title": i["title"],
            "description": i["description"],
            "link": i["link"]
        })
    return json.JSONEncoder().encode(result)


@app.route('/professions', methods=['GET'])
def professions():
    data = dbFetch("SELECT * FROM profession")

    result = []
    for i in data:
        result.append({
            "id": i["id"],
            "value": i["title"]
        })
    return json.JSONEncoder().encode(result)


def dbFetch(query):
    response = 'something wrong'

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
                cursor.execute(query)
                response = cursor.fetchall()
            connection.commit()

        finally:
            connection.close()

    except Exception as e:
        print(e)

    return response

"""Routes for Questions table."""
import flask
import BNTR_API
from BNTR_API.api.authenticate import verify_key


@BNTR_API.app.route('/api/questions/<game_id_slug>/', methods=['POST'])
def insert_question(game_id_slug):
    """Insert question into database."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    worth = msg['weight']
    decrease = msg['decrease']
    text = msg['question']
    opt1 = msg['opt1']
    opt2 = msg['opt2']
    opt3 = msg['opt3']
    time_dsg = msg['time_designation']
    answer = 'PENDING'

    connection.execute(
        "INSERT INTO questions(gameID, worth, decrease, text, opt1, opt2, opt3, answer, time_designation) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ",
        (game_id_slug, worth, decrease, text, opt1, opt2, opt3, answer, time_dsg, )
    )

    cur = connection.execute(
        "SELECT last_insert_rowid() ",
        ()
    )
    ques_id = cur.fetchone()

    connection.execute(
        "UPDATE games "
        "SET num_questions = num_questions + 1 "
        "WHERE gameID = ? ",
        (game_id_slug, )
    )

    context = {
        "text": text, 
        "opt1": opt1, 
        "opt2": opt2, 
        "opt3": opt3, 
        "questionID": ques_id['last_insert_rowid()'],
        "answer": answer
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/questions/update/<question_id_slug>/', methods=['POST'])
def update_question_answer(question_id_slug):
    """Update question answer in database."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    answer = msg['answer']

    cur = connection.execute(
        "UPDATE questions "
        "SET answer = ? "
        "WHERE questionID = ? "
        "RETURNING * ",
        (answer, question_id_slug, )
    )

    question = cur.fetchone()

    request_dict = {
        "answer": answer,
        "worth": question['worth'],
        "decrease": question['decrease']
    }

    context = update_answers_and_scores(question_id_slug, request_dict)

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/questions/<game_id_slug>/')
def fetch_questions_for_game(game_id_slug):
    """Fetch questions for a specific game."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM questions "
        "WHERE gameID = ? ",
        (game_id_slug, )
    )
    questions = cur.fetchall()

    context = {"questions": []}

    for ques in questions:
        dict_entry = {
            "questionID": ques['questionID'],
            "gameID": ques['gameID'],
            "worth": ques['worth'],
            "decrease": ques['decrease'],
            "text": ques['text'],
            "options": [ques['opt1'], ques['opt2'], ques['opt3']],
            "answer": ques['answer'],
            "time_designation": ques['time_designation']
        }
        context['questions'].append(dict_entry)
    
    return flask.jsonify(**context), 200


def update_answers_and_scores(question_id_slug, msg):
    """Update answer status and user scores."""
    connection = BNTR_API.model.get_db()
    correct_status = 'CORRECT'
    correct_worth = msg['worth']
    answer = msg['answer']

    cur = connection.execute(
        "UPDATE answers "
        "SET status = ? "
        "WHERE questionID = ? AND answer = ? "
        "RETURNING userID ",
        (correct_status, question_id_slug, answer, )
    )

    correct_users = cur.fetchall()

    for user in correct_users:
        connection.execute(
            "UPDATE users "
            "SET banter = banter + ? "
            "WHERE userID = ? ",
            (correct_worth, user['userID'], )
        )

    incorrect_status = 'INCORRECT'
    incorrect_worth = msg['decrease']
    
    cur = connection.execute(
        "UPDATE answers "
        "SET status = ? "
        "WHERE questionID = ? AND status != ? "
        "RETURNING userID ",
        (incorrect_status, question_id_slug, correct_status, )
    )

    incorrect_users = cur.fetchall()

    for user in incorrect_users:
        connection.execute(
            "UPDATE users "
            "SET banter = banter - ? "
            "WHERE userID = ? ",
            (incorrect_worth, user['userID'], )
        )
    
    context = {
        "num_correct": len(correct_users),
        "num_incorrect": len(incorrect_users),
        "increase": correct_worth,
        "decrease": incorrect_worth
    }

    return context
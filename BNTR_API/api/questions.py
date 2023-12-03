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

    question_stage = msg['question_stage']
    locked = "False"
    label = msg['label']
    text = msg['question']
    type = msg['type']
    tag = msg['tag']

    opt1, worth1, decrease1 = msg['opt1']
    opt2, worth2, decrease2 = msg['opt2']
    opt3 = 'NULL'
    worth3 = 0
    decrease3 = 0

    if 'opt3' in msg:
        opt3, worth3, decrease3 = msg['opt3']

    answer = 'PENDING'

    connection.execute(
        "INSERT INTO questions(gameID, locked, text, label, question_stage, opt1, worth1, decrease1, opt2, worth2, decrease2, opt3, worth3, decrease3, answer, type, tag) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
        (game_id_slug, locked, text, label, question_stage, opt1, worth1, decrease1, opt2, worth2, decrease2, opt3, worth3, decrease3, answer, type, tag, )
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
        "opts": [opt1, opt2, opt3], 
        "questionID": ques_id['last_insert_rowid()'],
        "answer": answer,
        "label": label,
        "stage": question_stage
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

    worth, decrease = get_values(answer, question)

    request_dict = {
        "answer": answer,
        "worth": worth,
        "decrease": decrease
    }

    context = update_answers_and_scores(question_id_slug, request_dict)

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/questions/<game_id_slug>/')
def fetch_questions_for_game(game_id_slug):
    """Fetch questions for a specific game."""
    if not (verify_key(flask.request.args.get('api_key'))):
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
            "locked": ques['locked'],
            "gameID": ques['gameID'],
            "label": ques['label'],
            "stage": ques['question_stage'],
            "text": ques['text'],
            "options": [ques['opt1'], ques['opt2'], ques['opt3']],
            "increases": [ques['worth1'], ques['worth2'], ques['worth3']],
            "decreases": [ques['decrease1'], ques['decrease2'], ques['decrease3']],
            "answer": ques['answer'],
            "type": ques['type'],
            "tag": ques['tag']
        }
        context['questions'].append(dict_entry)
    
    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/questions/<game_id_slug>/<stage_slug>/', methods=['POST'])
def update_questions_by_stage(game_id_slug, stage_slug):
    """Update question by question stage."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    connection.execute(
        "UPDATE questions "
        "SET locked = ? "
        "WHERE gameID = ? AND question_stage = ? ", 
        ("True", game_id_slug, stage_slug, )
    )
    
    context = {
        "msg": "update successful"
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/questions/<game_id_slug>/<user_id_slug>/')
def fetch_questions_by_user(game_id_slug, user_id_slug):
    """Fetch questions according to user answers."""
    if not (verify_key(flask.request.args.get('api_key'))):
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
    user_answer = None
    answered = None

    for ques in questions:

        cursor = connection.execute(
            "SELECT * "
            "FROM answers "
            "WHERE userID = ? AND questionID = ? ",
            (user_id_slug, ques['questionID'], )
        )
        answer = cursor.fetchone()
        if answer == None:
            user_answer = "NULL"
            answered = "False"
        else:
            user_answer = answer['answer']
            answered = "True"

        dict_entry = {
            "questionID": ques['questionID'],
            "locked": ques['locked'],
            "gameID": ques['gameID'],
            "label": ques['label'],
            "stage": ques['question_stage'],
            "text": ques['text'],
            "options": [ques['opt1'], ques['opt2'], ques['opt3']],
            "increases": [ques['worth1'], ques['worth2'], ques['worth3']],
            "decreases": [ques['decrease1'], ques['decrease2'], ques['decrease3']],
            "answer": ques['answer'],
            "user_answer": user_answer,
            "answered": answered, 
            "type": ques['type'],
            "tag": ques['tag']
        }
        context["questions"].append(dict_entry)
    
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


def get_values(answer, question):
    """Get increase and decrease values for respective answer."""
    if answer == 'opt1':
        worth = question['worth1']
        decrease = question['decrease1']
    elif answer == 'opt2':
        worth = question['worth2']
        decrease = question['decrease2']
    else:
        worth = question['worth3']
        decrease = question['decrease3']

    return worth, decrease
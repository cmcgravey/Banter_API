"""Routes for Answers table."""
import flask
import BNTR_API
from BNTR_API.api.authenticate import verify_key


@BNTR_API.app.route('/api/answers/<question_id_slug>/<user_id_slug>/', methods=['POST'])
def insert_answer(question_id_slug, user_id_slug):
    """Insert answer into database."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403

    connection = BNTR_API.model.get_db()

    answer = msg['answer']
    status = 'PENDING'

    connection.execute(
        "INSERT INTO answers(userID, questionID, answer, status) "
        "VALUES (?, ?, ?, ?) ",
        (user_id_slug, question_id_slug, answer, status, )
    )

    context = {
        "userID": user_id_slug, 
        "questionID": question_id_slug, 
        "answer": answer,
        "status": status 
    }

    return flask.jsonify(**context), 200


def update_answers_and_scores(question_id_slug):
    """Update answer status and user scores."""
    msg = flask.request.json

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
            "UPDATE answers "
            "SET banter = banter - ? "
            "WHERE userID + ? ",
            (incorrect_worth, user['userID'], )
        )
    
    context = {
        "num_correct": len(correct_users),
        "num_incorrect": len(incorrect_users),
        "increase": correct_worth,
        "decrease": incorrect_worth
    }

    return flask.jsonify(**context), 200









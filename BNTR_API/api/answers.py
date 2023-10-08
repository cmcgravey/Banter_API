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
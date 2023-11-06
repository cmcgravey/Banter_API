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


@BNTR_API.app.route('/api/answers/<question_id_slug>/<user_id_slug>/')
def fetch_answer(question_id_slug, user_id_slug):
    """Determine if user has answered a particular question."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT userID, answer "
        "FROM answers "
        "WHERE userID = ? AND questionID = ? ",
        (user_id_slug, question_id_slug, )
    )
    answer = cur.fetchall()

    context = {
        "answered": False,
        "answer": None
    }
    
    if answer != []:
        context['answered'] = True
        context['answer'] = answer[0]['answer']
    
    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/answers/game/<game_id_slug>/<user_id_slug>/')
def fetch_answers(game_id_slug, user_id_slug):
    """Fetch all of user's answers for given game."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT questionID "
        "FROM questions "
        "WHERE gameID = ? ",
        (game_id_slug, )
    )
    questionids = cur.fetchall()

    context = {}

    for question in questionids:
        qid = question['questionID']

        cur = connection.execute(
            "SELECT userID "
            "FROM answers "
            "WHERE questionID = ? AND userID = ? ",
            (qid, user_id_slug, )
        )
        uid = cur.fetchone()

        if 'userID' in uid:
            context[qid] = True
        else: 
            context[qid] = False
    
    return flask.jsonify(**context), 200

"""Routes for games table."""
import flask 
import BNTR_API
from BNTR_API.api.authenticate import verify_key

@BNTR_API.app.route('/api/games/', methods=['POST'])
def insert_game():
    """Insert game into the database."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    teamid1 = msg['teamid1']
    teamid2 = msg['teamid2']
    status = 'PENDING'
    num_questions = 0

    connection.execute(
        "INSERT INTO games(teamID1, teamID2, status, num_questions) "
        "VALUES (?, ?, ?, ?) ",
        (teamid1, teamid2, status, num_questions, )
    )

    cur = connection.execute(
        "SELECT last_insert_rowid() ",
        ()
    )

    lastid = cur.fetchone()

    context = {
        "id": lastid['last_insert_rowid()'],
        "team1": teamid1,
        "team2": teamid2
    }

    return flask.jsonify(**context), 200

@BNTR_API.app.route('/api/games/<game_id_slug>/', methods=['POST'])
def update_game(game_id_slug):
    """Update game status or questions."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()
    type = msg['type']

    if type == 'questions':
        new_num = msg['update']
        cur = connection.execute(
            "UPDATE games "
            "SET num_questions = ? "
            "WHERE gameID =  ? "
            "RETURNING * ",
            (new_num, game_id_slug, )
        )
        game_update = cur.fetchall()

    else:
        new_status = msg['update']
        cur = connection.execute(
            "UPDATE games "
            "SET status = ? "
            "WHERE gameID = ? "
            "RETURNING * ",
            (new_status, game_id_slug, )
        )
        game_update = cur.fetchall()
    
    context = {
        "gameID": game_update[0]['gameID'],
        "team1": game_update[0]['teamID1'],
        "team2": game_update[0]['teamID2'],
        "status": game_update[0]['status'],
        "num_questions": game_update[0]['num_questions']
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/games/<game_id_slug>/')
def retrieve_game(game_id_slug):
    """Retrieve game from database."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM games "
        "WHERE gameID = ? ",
        (game_id_slug, )
    )

    game_info = cur.fetchall()

    context = {
        "gameID": game_id_slug,
        "teamID1": game_info[0]['teamID1'],
        "teamID2": game_info[0]['teamID2'],
        "status": game_info[0]['status'],
        "num_questions": game_info[0]['num_questions']
    }

    return flask.jsonify(**context), 200

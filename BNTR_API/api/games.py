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

    fixtureID = msg['fixtureID']
    teamid1 = msg['teamID1']
    teamid2 = msg['teamID2']
    league = msg['league']
    team1_score = 0
    team2_score = 0
    time_elapsed = '00:00'
    status = 'PENDING'
    num_questions = 0

    connection.execute(
        "INSERT INTO games(fixtureID, league, teamID1, teamID2, team1_score, team2_score, time_elapsed, status, num_questions) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ",
        (fixtureID, league, teamid1, teamid2, team1_score, team2_score, time_elapsed, status, num_questions, )
    )

    cur = connection.execute(
        "SELECT last_insert_rowid() ",
        ()
    )

    lastid = cur.fetchone()

    context = {
        "id": lastid['last_insert_rowid()'],
        "team1": teamid1,
        "team2": teamid2,
        "fixtureID": fixtureID
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

    new_status = msg['update']
    cur = connection.execute(
        "UPDATE games "
        "SET team1_score = ?, team2_score = ?, time_elapsed = ? "
        "WHERE gameID = ? "
        "RETURNING * ",
        (new_status[0], new_status[1], new_status[2], game_id_slug, )
    )
    game_update = cur.fetchall()

    if 'status' in msg:
        cur = connection.execute(
            "UPDATE games "
            "SET status = ? "
            "WHERE gameID = ? "
            "RETURNING * ",
            (msg['status'], game_id_slug, )
        )
        game_update = cur.fetchall()
    
    context = {
        "gameID": game_update[0]['gameID'],
        "team1": game_update[0]['teamID1'],
        "team1_score": game_update[0]['team1_score'],
        "team2": game_update[0]['teamID2'],
        "team2_score": game_update[0]['team2_score'],
        "time_elapsed": game_update[0]['time_elapsed'],
        "status": game_update[0]['status'],
        "num_questions": game_update[0]['num_questions']
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/games/<game_id_slug>/')
def retrieve_game(game_id_slug):
    """Retrieve game from database."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM games "
        "WHERE gameID = ? ",
        (game_id_slug, )
    )

    game_info = cur.fetchone()

    teamids = [game_info['teamID1'], game_info['teamID2']]
    names = []
    for num in teamids:
        cur = connection.execute(
            "SELECT name "
            "FROM teams "
            "WHERE teamID = ? ",
            (num, )
        )
        name = cur.fetchone()['name']
        names.append(name)

    context = {
        "gameID": int(game_id_slug),
        "league": game_info['league'],
        "teamID1": game_info['teamID1'],
        "team1_name": names[0],
        "team1_score": game_info['team1_score'],
        "teamID2": game_info['teamID2'],
        "team2_name": names[1],
        "team2_score": game_info['team2_score'],
        "time_elapsed": game_info['time_elapsed'],
        "status": game_info['status'],
        "num_questions": game_info['num_questions']
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/games/status/<status>/')
def fetch_games(status):
    """Fetch all games of a certain status."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM games "
        "WHERE status = ? "
        "ORDER BY gameID ASC",
        (status, )
    )
    games = cur.fetchall()

    context = {"games": []}

    for game in games:
        teamids = [game['teamID1'], game['teamID2']]
        names = []
        for num in teamids:
            cur = connection.execute(
                "SELECT name "
                "FROM teams "
                "WHERE teamID = ? ",
                (num, )
            )
            name = cur.fetchone()['name']
            names.append(name)

        dict_entry = {
            "gameID": game['gameID'],
            "league": game['league'],
            "teamID1": game['teamID1'],
            "team1_name": names[0],
            "team1_score": game['team1_score'],
            "teamID2": game['teamID2'],
            "team2_name": names[1],
            "team2_score": game['team2_score'],
            "time_elapsed": game['time_elapsed'],
            "status": game['status'],
            "num_questions": game['num_questions'],
        }
        context['games'].append(dict_entry)
    
    return flask.jsonify(**context), 200

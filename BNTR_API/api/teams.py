"""Routes for Teams table."""
import flask
import BNTR_API
from BNTR_API.api.authenticate import verify_key

@BNTR_API.app.route('/api/teams/', methods=['POST'])
def insert_team():
    """Insert a team into the database."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403


    connection = BNTR_API.model.get_db()

    name = msg['name']
    abbr = msg['abbr']
    logo = msg['logo']

    connection.execute(
        "INSERT INTO teams(logo, name, abbr) "
        "VALUES (?, ?, ?) ",
        (logo, name, abbr, )
    )

    cur = connection.execute(
        "SELECT last_insert_rowid() ",
        ()
    )

    last_id = cur.fetchone()

    context = {
        "teamid": last_id['last_insert_rowid()'],
        "name": name
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/teams/<team_id_slug>/')
def get_team(team_id_slug):
    """Retrieve team from the database."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403

    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM teams "
        "WHERE teamID = ? ",
        (team_id_slug, )
    )

    team_info = cur.fetchall()

    context = {
        "name": team_info[0]['name'],
        "abbr": team_info[0]['abbr'],
        "logo": team_info[0]['logo'],
        "id": team_info[0]['teamID']
    }

    return flask.jsonify(**context), 200


    

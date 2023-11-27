"""Routes for Search page."""
import flask
import BNTR_API
from BNTR_API.api.authenticate import verify_key


@BNTR_API.app.route('/api/search/<username>/')
def fetch_by_username(username):
    """Fetch user by username."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    username = username + '%'

    cur = connection.execute(
        "SELECT * "
        "FROM Users "
        "WHERE username "
        "like ? ",
        (username, )
    )

    results = cur.fetchall()
    context = {"results": []}

    for result in results:
        entry = {}
        entry['userID'] = result['userID']
        entry['username'] = result['username']
        entry['banter'] = result['banter']
        context["results"].append(entry)

    return flask.jsonify(**context), 200

"""Routes for users table."""
import flask 
import BNTR_API
from BNTR_API.api.authenticate import verify_key, hash_password, verify_password
from BNTR_API.api.following import get_num_followers_following

@BNTR_API.app.route('/api/users/', methods=['POST'])
def insert_user():
    """Insert user into database."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    username = msg['username']
    password = hash_password(msg['password'])
    full_name = msg['full_name']
    profile_picture = msg['prof_pic']

    banter = 20

    connection.execute(
        "INSERT INTO users(username, password, banter, fullname, profile_picture) "
        "VALUES (?, ?, ?, ?, ?) ",
        (username, password, banter, full_name, profile_picture, )
    )

    cur = connection.execute(
        "SELECT last_insert_rowid() ",
        ()
    )

    lastid = cur.fetchone()

    context = {
        "userID": lastid['last_insert_rowid()'],
        "username": username, 
        "banter": banter, 
        "full_name": full_name, 
        "profile_picture": profile_picture
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/users/<user_id_slug>/', methods=['POST'])
def update_password(user_id_slug):
    """Update user's password."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()
    type = msg['type']

    if (type == 'password'):
        new_password = hash_password(msg['new_password'])

        cur = connection.execute(
            "UPDATE users "
            "SET password = ? "
            "WHERE userID = ? "
            "RETURNING * ",
            (new_password, user_id_slug, )
        )

    else: 
        new_score = msg['new_banter']

        cur = connection.execute(
            "UPDATE users "
            "SET banter = ? "
            "WHERE userID = ? "
            "RETURNING * ",
            (new_score, user_id_slug, )
        )


    user_update = cur.fetchone()

    context = {
        "userID": user_update['userID'],
        "username": user_update['username'],
        "banter": user_update['banter']
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/users/logon/', methods=['POST'])
def verify_user():
    """Verify user information."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    username = msg['username']
    password = msg['password']

    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )

    user_info = cur.fetchone()

    if user_info == []:
        context = {
            "msg": "Invalid user"
        }
        return flask.jsonify(**context), 200
    elif verify_password(user_info['password'], password):
        context = {
            "userID": user_info['userID'],
            "username": username, 
            "banter": user_info['banter']
        }
        return flask.jsonify(**context), 200
    else:
        context = {
            "msg": "Invalid password"
        }
        return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/users/<user_id_slug>/')
def fetch_user(user_id_slug):
    """Fetch user information."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE userID = ? ",
        (user_id_slug, )
    )
    info = cur.fetchone()
    followers, following = get_num_followers_following(connection, user_id_slug)

    context = {
        "userID": user_id_slug, 
        "username": info['username'], 
        "banter": info['banter'],
        "full_name": info['fullname'],
        "profile_picture": info['profile_picture'], 
        "num_followers": followers, 
        "num_following": following
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/users/leaders/')
def fetch_leaderboards():
    """Fetch leaderboard information."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "ORDER BY banter DESC, username DESC ",
        ()
    )
    leaders = cur.fetchall()

    context = {"leaders": []}

    for idx, user in enumerate(leaders):
        if idx == 8:
            break

        context['leaders'].append({"name": user['username'], "banter": user['banter'], "profile_picture": user['profile_picture'], "userID": user['userID']})

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/users/leaderboards/following/<user_id_slug>/')
def fetch_following_leaderboards(user_id_slug):
    """Fetch leaderboards of all users loguser is following."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT U.username, U.banter, U.userID, U.profile_picture "
        "FROM Users U "
        "JOIN Following F ON U.userID = F.userID2 "
        "WHERE F.userID1 = ? "
        "UNION ALL "
        "SELECT U2.username, U2.banter, U2.userID, U2.profile_picture "
        "FROM Users U2 "
        "WHERE U2.userID = ? "
        "ORDER BY banter DESC ",
        (user_id_slug, user_id_slug, )
    )
    following = cur.fetchall()

    context = {"leaders": []}

    for idx, user in enumerate(following):
        if idx == 8:
            break

        context['leaders'].append({"name": user['username'], "banter": user['banter'], "profile_picture": user['profile_picture'], "userID": user['userID']})

    return flask.jsonify(**context), 200
"""Routes for Search page."""
import flask
import BNTR_API
from BNTR_API.api.authenticate import verify_key


@BNTR_API.app.route('/api/following/', methods=['POST'])
def add_relationship():
    """Add new following relation to database."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    userID1 = msg['userID1']
    userID2 = msg['userID2']

    connection = BNTR_API.model.get_db()

    connection.execute(
        "INSERT INTO Following(userID1, userID2) "
        "VALUES (?, ?) ",
        (userID1, userID2)
    )

    context = {
        "msg": "Insert Success"
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/unfollowing/', methods=['POST'])
def remove_relationship(): 
    """Remove following relationship from database."""
    msg = flask.request.json

    if not (verify_key(msg['api_key'])):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    userID1 = msg['userID1']
    userID2 = msg['userID2']

    connection = BNTR_API.model.get_db()

    connection.execute(
        "DELETE "
        "FROM Following "
        "WHERE userID1 = ? AND userID2 = ? ",
        (userID1, userID2, )
    )

    context = {
        "msg": "deletion success"
    }

    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/followers/<user_id_slug>/')
def fetch_followers(user_id_slug):
    """Fetch all followers for User."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403    

    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT U.userID, U.username, U.banter, U.profile_picture "
        "FROM Users U, Following F "
        "WHERE F.userID1 = U.userID AND F.userID2 = ? ",
        (user_id_slug, )
    )
    followers = cur.fetchall()

    context = {"followers": []}

    for follower in followers: 
        context['followers'].append({"userID": follower['userID'],
                                     "username": follower['username'],
                                     "banter": follower['banter'],
                                     "profile_picture": follower['profile_picture']})
    
    return flask.jsonify(**context), 200


@BNTR_API.app.route('/api/following/<user_id_slug>/')
def fetch_following(user_id_slug):
    """Fetch all following for User."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT U.userID, U.username, U.banter, U.profile_picture "
        "FROM Users U, Following F "
        "WHERE F.userID2 = U.userID AND F.userID1 = ? ",
        (user_id_slug, )
    )
    following = cur.fetchall()

    context = {"following": []}

    for follow in following:
        context['following'].append({
            "userID": follow['userID'],
            "username": follow['username'],
            "banter": follow['banter'],
            "profile_picture": follow['profile_picture']
        })
    return flask.jsonify(**context), 200


def get_num_followers_following(connection, userIdSlug):
    """Get number of followers and following for user."""
    cur = connection.execute(
        "SELECT * "
        "FROM Following "
        "WHERE userID2 = ? ",
        (userIdSlug, )
    )
    followers = cur.fetchall()
    num_followers = len(followers)

    cur = connection.execute(
        "SELECT * "
        "FROM Following "
        "WHERE userID1 = ? ",
        (userIdSlug, )
    )
    following = cur.fetchall()
    num_following = len(following)

    return num_followers, num_following


def get_logname_follows(connection, userIDSlug, followedUser):
    """Determine if userIDSlug follows followedUser."""
    cur = connection.execute(
        "SELECT * "
        "FROM Following "
        "WHERE userID1 = ? AND userID2 = ? ",
        (userIDSlug, followedUser, )
    )
    lognamefollows = cur.fetchone()
    logname_follows_username = False

    if lognamefollows is not None: 
        logname_follows_username = True
    
    return logname_follows_username
    

@BNTR_API.app.route('/api/users/<logged_user>/<userIdSlug>/')
def fetchUserInfo(logged_user, userIdSlug):
    """Fetch user other than logged user."""
    if not (verify_key(flask.request.args.get('api_key'))):
        context = {'msg': 'invalid key'}
        return flask.jsonify(**context), 403
    
    connection = BNTR_API.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM Users "
        "WHERE userID = ? ",
        (userIdSlug, )
    )
    info = cur.fetchone()
    lfu = get_logname_follows(connection, logged_user, userIdSlug)
    followers, following = get_num_followers_following(connection, userIdSlug)

    context = {
        "userID": userIdSlug, 
        "username": info['username'], 
        "banter": info['banter'],
        "full_name": info['fullname'],
        "profile_picture": info['profile_picture'],
        "logname_follows_username": lfu, 
        "num_followers": followers, 
        "num_following": following
    }

    return flask.jsonify(**context), 200
"""Display all possible routes for API."""
import flask
import BNTR_API

@BNTR_API.app.route('/api/routes/')
def show_routes():
    """Show resource urls."""

    context = {
        "teams": "POST /api/teams/ for insertion GET /api/teams/ for retrieval",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }

    print('here')
    
    return flask.jsonify(**context), 200
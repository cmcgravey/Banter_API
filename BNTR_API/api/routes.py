"""Display all possible routes for API."""
import flask
import BNTR_API

@BNTR_API.app.route('/api/routes/')
def show_routes():
    """Show resource urls."""

    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    
    return flask.jsonify(**context)
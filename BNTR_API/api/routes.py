"""Display all possible routes for API."""
import flask
import BNTR_API

@BNTR_API.app.route('/api/routes/')
def show_routes():
    """Show resource urls."""

    context = {
        "routes": "GET /api/routes/",
        "users": [
            {"insert_user": "POST /api/users/"},
            {"fetch_user": "GET /api/users/<user_id_slug>/"},
            {"update_user": "POST /api/users/<user_id_slug>/"},
            {"logon_user": "POST /api/users/logon/"}
        ],
        "teams": [
            {"insert_team": "POST /api/teams/"}, 
            {"fetch_team": "GET /api/teams"}
        ],
        "games": [
            {"insert_game": "POST /api/games/"},
            {"update_game": "POST /api/games/<game_id_slug>/"},
            {"fetch_one": "GET /api/games/<game_id_slug>/"},
            {"fetch_multiple": "GET /api/games/"}
        ], 
        "answers": [
            {"insert_answer": "POST /api/answers/<question_id_slug>/"}
        ],
        "questions": [
            {"insert_question": "POST /api/questions/<game_id_slug>/"},
            {"update_question_answer": "POST /api/questions/update/<question_id_slug>/"},
            {"fetch_game_questions": "GET /api/questions/<game_id_slug>/"}
        ]
    }
    
    return flask.jsonify(**context), 200
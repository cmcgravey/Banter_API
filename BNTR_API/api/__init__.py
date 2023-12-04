"""Routes for BNTR API."""
from BNTR_API.api.routes import show_routes
from BNTR_API.api.teams import insert_team
from BNTR_API.api.games import insert_game, update_game, retrieve_game
from BNTR_API.api.users import insert_user, update_password, fetch_user, verify_user, fetch_following_leaderboards, fetch_leaderboards
from BNTR_API.api.questions import insert_question, update_question_answer, fetch_questions_for_game
from BNTR_API.api.answers import insert_answer
from BNTR_API.api.search import fetch_by_username
from BNTR_API.api.following import add_relationship, fetch_followers, fetch_following, fetchUserInfo, remove_relationship
"""Routes for BNTR API."""
from BNTR_API.api.routes import show_routes
from BNTR_API.api.teams import insert_team
from BNTR_API.api.games import insert_game, update_game, retrieve_game
from BNTR_API.api.users import insert_user, update_password, fetch_user, verify_user
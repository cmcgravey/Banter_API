"""BNTR_API Package Initializer."""
import flask

app = flask.Flask(__name__)

app.config.from_object('BNTR_API.config')

app.config.from_envvar('BNTR_API_SETTINGS', silent=True)

import BNTR_API.api
import BNTR_API.model
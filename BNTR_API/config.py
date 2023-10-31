"""BNTR_API Development Configuration."""
import pathlib

API_KEY = '87ab0a3db51d297d3d1cf2d4dcdcb71b'

APPLICATION_ROOT = '/api/routes/'

BNTR_API_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BNTR_API_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

DATABASE_FILENAME = BNTR_API_ROOT/'var'/'BNTR_API.sqlite3'

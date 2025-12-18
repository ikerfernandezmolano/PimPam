import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DB_PATH = os.path.join(BASE_DIR, "library.db")
    SECRET_KEY = "supersecretkey"


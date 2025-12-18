from werkzeug.security import generate_password_hash

from app.model.book_model import Book


class UserController:

    def __init__(self, db):
        self.db = db

    @staticmethod
    def create_user(self, name):
        if not name or len(name.strip() < 3):
            raise ValueError('El nombre debe tener al menos 3 caracteres.')

        self.db.insert(
            sentence="INSERT INTO users (name) VALUES (?)",
            parameters=[name.strip()]
        )

    def get_all(self):
        return self.db.select(
            sentence="SELECT * FROM users"
        )
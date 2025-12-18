import sqlite3

from app.database.db_connection import Connection


class Book:
    def __init__(self, book_id, book_title, book_author):
        self.book_id = id
        self.book_title = book_title
        self.book_author = book_author

    @staticmethod
    def get_all_books():
        conn = Connection()
        sentence = "SELECT * FROM books"
        rows = conn.select(sentence=sentence)
        return [
            Book(
                book_id=row['id'],
                book_title=row['title'],
                book_author=row['author']
            ) for row in rows
        ]

    @staticmethod
    def get_book_by_id(book_id):
        conn = Connection()
        row = conn.select(
            sentence="SELECT * FROM books WHERE id = ?",
            parameters=[book_id]
        )

        if row:
            Book(
                book_id=row['id'],
                book_title=row['title'],
                book_author=row['author']
            )
        return None

    @staticmethod
    def get_book_by_title(book_title):
        conn = Connection()
        row = conn.select(
            sentence="SELECT * FROM books WHERE title = ?",
            parameters=[book_title]
        )

        if row:
            return Book(
                book_id=row['id'],
                book_title=row['title'],
                book_author=row['author']
            )
        return None

    @staticmethod
    def create_book(book_title, book_author):
        conn = Connection()
        conn.insert(
            sentence="INSERT INTO books (title) VALUES (?)",
            parameters=[book_title, book_author]
        )

    @staticmethod
    def delete_book_by_id(user_id):
        conn = Connection()
        conn.delete(
            sentence="DELETE FROM books WHERE id = ?",
            parameters=[user_id]
        )

    @staticmethod
    def update_field(user_id, field, new_value):
        conn = Connection()
        try:
            conn.update(
                sentence=f"UPDATE users SET {field}=? WHERE id=?",
                parameters=[new_value, user_id]
            )
            return True, None
        except sqlite3.IntegrityError as e:
            if "title" in str(e).lower():
                return False, "Title already in use"
            elif "author" in str(e).lower():
                return False, "Email already in use"
            return False, "An error occurred, could not update the field"
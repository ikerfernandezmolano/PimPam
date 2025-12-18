class BookController:

    def __init__(self, db):
        self.db = db

    def create_book(self, title, copies):
        if not title or copies<=0:
            raise ValueError("Datos inválidos")

        self.db.insert(
            sentence="INSERT INTO books (title, total_copies) VALUES (?, ?)",
            parameters=[title.strip, copies]
        )

    def get_all(self):
        return self.db.select(
            sentence="SELECT * FROM books"
        )
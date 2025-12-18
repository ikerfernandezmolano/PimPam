from datetime import date, timedelta


class LoanController:
    MAX_ACTIVE_LOANS = 3
    LOAN_DAYS = 14

    def __init__(self, db):
        self.db = db

    def create_loan(self, user_id, book_id):
        active = self.db.select(
            sentence="SELECT COUNT(*) FROM loans WHERE user_id = ? AND status = 'ACTIVE'",
            parameters=[user_id]
        ).fetchone()[0]

        if active >= self.MAX_ACTIVE_LOANS:
            raise ValueError("El usuario ha alcanzado el máximo de préstamos")

        self.db.insert(
            sentence="INSERT INTO loans (user_id, book_id, status) VALUES (?, ?, ?)",
            parameters=[user_id, book_id, 'ACTIVE']
        )

    def get_all(self):
        return self.db.select(
            sentence="""SELECT loans.id, users.name, books.title ,loans.status 
                        FROM loans 
                        JOIN users ON users.id = loans.user_id 
                        JOIN books ON books.id = loans.book_id"""
        )
class GestorUsuarios:

    def __init__(self, db):
        self.db = db

    def registrarUsuario(self, user, email, passwd):
        self.db.insert(
            sentence="INSERT INTO Usuario (Nombre, Email, Contrasena,Estado) VALUES (?,?,?,?)",
            parameters=[user.strip(),email.strip(),passwd.strip(),"Espera"]
        )

    def get_all(self):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario"
        )

        return [ dict(row) for row in rows ]

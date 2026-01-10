class Usuario:
    def __init__(self, IDUsuario, Nombre, Email, Contrasena, Estado='Espera', IDFavorito=1):
        self.IDUsuario = IDUsuario
        self.Nombre = Nombre
        self.Email = Email
        self.Contrasena = Contrasena
        self.Estado = Estado
        self.IDFavorito = IDFavorito


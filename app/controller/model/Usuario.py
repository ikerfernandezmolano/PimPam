class Usuario:
    def __init__(self, IDUsuario, Nombre, Email, Contrasena, Estado='Espera', Favorito="Bulbasaur"):
        self.IDUsuario = IDUsuario
        self.Nombre = Nombre
        self.Email = Email
        self.Contrasena = Contrasena
        self.Estado = Estado
        self.Favorito = Favorito
        
    def getData(self):
        return {
            "IDUsuario": self.IDUsuario,
            "Nombre": self.Nombre,
            "Email": self.Email,
            "Contrasena": self.Contrasena,
            "Estado": self.Estado,
            "Favorito": self.Favorito
        }


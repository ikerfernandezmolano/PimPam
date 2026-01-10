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
    
    def editUser(self, pEmail, pContraseña, pNombrePKFav, pEstado):
            if pEmail != '' and pEmail is not None:
                self.Email = pEmail
            if pContraseña != '' and pContraseña is not None:
                self.Contrasena = pContraseña
            if pNombrePKFav != '' and pNombrePKFav  is not None:
                self.Favorito = pNombrePKFav
            if pEstado != '' and pEstado is not None:
                self.Estado = pEstado


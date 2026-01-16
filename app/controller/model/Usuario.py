class Usuario:
    def __init__(self, pIDUsuario, pNombre, pEmail, pContrasena, pEstado='Espera', pFavorito="Bulbasaur"):
        self.IDUsuario = pIDUsuario
        self.Nombre = pNombre
        self.Email = pEmail
        self.Contrasena = pContrasena
        self.Estado = pEstado
        self.Favorito = pFavorito
        
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


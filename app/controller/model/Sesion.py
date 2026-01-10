class Sesion:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.usuario = None  # Aquí guardaremos la instancia de Usuario
        return cls._instance

    def startSession(self, pIDUsuario, pNombre, pEmail, pContraseña, pAREA='Espera', pNombrePKFav=1):
        """Crea la instancia de Usuario y la guarda en la sesión"""
        from app.controller.model.Usuario import Usuario  # importa tu clase Usuario
        self.usuario = Usuario(
            IDUsuario=pIDUsuario,
            Nombre=pNombre,
            Email=pEmail,
            Contrasena=pContraseña,
            Estado=pAREA,
            IDFavorito=pNombrePKFav
        )

    def cerrar(self):
        """Cerrar sesión"""
        self.usuario = None

    def esta_logueado(self):
        return self.usuario is not None


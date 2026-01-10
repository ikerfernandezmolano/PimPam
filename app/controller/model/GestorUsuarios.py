class GestorUsuarios:

    def __init__(self, db):
        self.db = db

    def añadirUsuario(self, user, email, passwd):
        try:
            self.db.insert(
                sentence="INSERT INTO Usuario (Nombre, Email, Contrasena,Estado) VALUES (?,?,?,?)",
                parameters=[user.strip(),email.strip(),passwd.strip(),"Espera"]
            )
            return 0
        except Exception as e:
            msg = str(e)

            if "Usuario.Nombre" in msg:
                return 1  # nombre repetido
            elif "Usuario.Email" in msg:
                return 2  # email repetido
            else:
                return 3  # otro error de integridad
        
    def iniciarSesion(self, email, passwd):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario WHERE Email=? LIMIT 1",
            parameters=[email.strip()]
        )

        if not rows:
            # Usuario no encontrado
            return 1

        usuario = rows[0]  # tomamos la primera fila

        if passwd.strip() != usuario['Contrasena']:
            # Contraseña incorrecta
            return 2
            
        if usuario['Estado'] != 'Aceptado' and usuario['Estado'] != 'Admin':
            return 3

        # Contraseña correcta
        from app.controller.model.Sesion import Sesion
        sesion = Sesion()
        sesion.startSession(
            pIDUsuario=usuario['IDUsuario'],
            pNombre=usuario['Nombre'],
            pEmail=usuario['Email'],
            pContraseña=usuario['Contrasena'],
            pAREA=usuario['Estado'],
            pNombrePKFav=usuario['IDFavorito']
        )
        from app.controller.model.GestorEspecies import GestorEspecies
        ge = GestorEspecies(self.db).initialize()
        return 0


    def get_all(self):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario"
        )

        return [ dict(row) for row in rows ]

from app.controller.model.Sesion import Sesion

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
            
        from app.controller.model.GestorEspecies import GestorEspecies
        ge = GestorEspecies(self.db).initialize()

        # Contraseña correcta
        nombre = self.db.select(
            sentence="SELECT Nombre FROM Especie WHERE PokedexID=? LIMIT 1",
            parameters=[usuario['IDFavorito']]
        )
        
        sesion = Sesion()
        sesion.startSession(
            pIDUsuario=usuario['IDUsuario'],
            pNombre=usuario['Nombre'],
            pEmail=usuario['Email'],
            pContraseña=usuario['Contrasena'],
            pAREA=usuario['Estado'],
            pNombrePKFav=nombre[0]['Nombre']
        )
        return 0
    
    def modificarDatos(self, email, password_old, password_new, pkFav=None):
        sesion = Sesion().getSession()

        # Si no se pasa pkFav, se busca el favorito actual
        if pkFav is None or pkFav == '':
            pkFavAux = sesion['Favorito']
            resultado = self.db.select(
                sentence="SELECT IDPokedex FROM Especie WHERE Nombre=?",
                parameters=[pkFavAux]
            )
            if resultado:
                pkFav = resultado[0]["IDPokedex"]
            else:
                pkFav = 1  # valor por defecto

        # Si se quiere cambiar la contraseña, se valida la vieja
        if password_old != '' and password_new != '':
            if password_old.strip() != sesion['Contrasena'].strip():
                return 1  # contraseña antigua incorrecta

        try:
            if password_new == '' or password_old == '':
                password_new = sesion['Contrasena']
            self.db.update(
                sentence="UPDATE Usuario SET Email=?, Contrasena=?, IDFavorito=? WHERE IDUsuario=?",
                parameters=[email, password_new, pkFav, sesion['IDUsuario']]
            )
            Sesion().editSession(pEmail=email , pContraseña=password_new, pNombrePKFav=pkFavAux)
            return 0  # éxito
        except Exception as e:
            msg = str(e)
            if "Usuario.Email" in msg:
                return 2  # email repetido
            else:
                return msg  # otro error de integridad

        
    def getSession(self):
        return Sesion().getSession()


    def get_all(self):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario"
        )

        return [ dict(row) for row in rows ]

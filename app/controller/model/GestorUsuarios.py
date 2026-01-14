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

        # --- FAVORITO ---
        if not pkFav:
            pkFavSes = sesion['Favorito']
            pkFav = self.db.select(
                sentence="SELECT PokedexID FROM Especie WHERE Nombre=? LIMIT 1",
                parameters=[pkFavSes]
            )[0]['PokedexID']
        else:
            pkFavSes=pkFav
            pkFav = self.db.select(
                sentence="SELECT PokedexID FROM Especie WHERE Nombre=? LIMIT 1",
                parameters=[pkFav]
            )[0]['PokedexID']

        # --- CONTRASEÑA ---
        if password_new.strip():
            if not password_old:
                return 3
            else:
                if password_old.strip() != sesion['Contrasena'].strip():
                    return 1
        else:
            password_new = sesion['Contrasena']
            
        
        # --- UPDATE ---
        try:
            self.db.update(
                sentence="UPDATE Usuario SET Email=?, Contrasena=?, IDFavorito=? WHERE IDUsuario=?",
                parameters=[email, password_new, pkFav, sesion['IDUsuario']]
            )

            Sesion().editSession(
                pEmail=email,
                pContraseña=password_new,
                pNombrePKFav=pkFavSes,
                pEstado=''
            )
            return 0

        except Exception as e:
            if "Usuario.Email" in str(e):
                return 2  # email repetido
            return str(e)
        
    def getSession(self):
        return Sesion().getSession()
        
    def borrarUsuario(self, idUser):
        self.db.delete(sentence="DELETE FROM Usuarios WHERE IDUsuario=?",
        parameters=[idUser]
        )


    def get_all(self):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario"
        )

        return [ dict(row) for row in rows ]
        
    def get_aceptados(self):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario WHERE Estado = 'Aceptado'"
        )

        return [ dict(row) for row in rows ]
        
    def get_espera(self):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario WHERE Estado = 'Espera' OR Estado = 'Rechazado'"
        )

        return [ dict(row) for row in rows ]
        
    def aceptar(self, user_id):
        self.db.update(
            sentence="UPDATE Usuario SET Estado = 'Aceptado' WHERE IDUsuario = ?",
            parameters=[user_id]
        )
        
    def rechazar(self, user_id):
        self.db.update(
            sentence="UPDATE Usuario SET Estado = 'Rechazado' WHERE IDUsuario = ?",
            parameters=[user_id]
        )
    
    def eliminar(self, user_id):
        self.db.delete(
            sentence="DELETE FROM Usuario WHERE IDUsuario = ?",
            parameters=[user_id]
        )
        
    def get_usuario(self, user_id):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario WHERE IDUsuario = ?",
            parameters=[user_id]
        )
        
        return {
            "IDUsuario": rows[0]["IDUsuario"],
            "Nombre": rows[0]["Nombre"],
            "Email": rows[0]["Email"],
            "Contrasena": rows[0]["Contrasena"],
            "Estado": rows[0]["Estado"],
            "IDFavorito": rows[0]["IDFavorito"]
        }
        
    def modificarDatosAdmin(self, email, password, pkFav=None, user_id=1):
        sesion = Sesion().getSession()
        usuario = self.get_usuario(user_id)
        if sesion['Estado'] == 'Admin':
            # --- FAVORITO ---
            if not pkFav:
                pkFav = usuario.IDFavorito
            else:
                pkFav = self.db.select(
                    sentence = "SELECT PokedexID FROM Especie WHERE Nombre = ? LIMIT 1",
                    parameters = [pkFav]
                )[0]['PokedexID']
            if not password:
                password = usuario['Contrasena']
                
            # --- UPDATE ---
            try:
                self.db.update(
                    sentence="UPDATE Usuario SET Email=?, Contrasena=?, IDFavorito=? WHERE IDUsuario=?",
                    parameters=[email, password, pkFav, user_id]
                )
                return 0

            except Exception as e:
                if "Usuario.Email" in str(e):
                    return 1  # email repetido
                return str(e)
        else:
            return 2
        
        
        

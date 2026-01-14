from app.controller.model.Sesion import Sesion

class GestorUsuarios:

    def __init__(self, db):
        self.db = db
        
#-----------------------AÑADIR/ELIMINAR USUARIO-----------------------------#

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
                
    def borrarUsuario(self, idUser):
        self.db.delete(sentence="DELETE FROM Usuarios WHERE IDUsuario=?",
        parameters=[idUser]
        )
                
#-----------------------------INICIAR SESIÓN----------------------------------#
        
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
        
#-----------------------------GETTERS INFO----------------------------------#
     
    def get_all(self):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario"
        )

        return [ dict(row) for row in rows ]
        
    def getSession(self):
        return Sesion().getSession()
        
    def get_usuario(self, user_id):
        rows = self.db.select(
            sentence="SELECT * FROM Usuario WHERE IDUsuario = ?",
            parameters=[user_id]
        )
        
        return {
            "IDUsuario": rows[0]["IDUsuario"],
            "Nombre": rows[0]["Nombre"],
            "Email": rows[0]["Email"],
            "Estado": rows[0]["Estado"],
            "IDFavorito": rows[0]["IDFavorito"]
        }
        
#---------------------------------FRIENDS-------------------------------------#
#------------------------------GETTERS INFO-----------------------------------#

    def get_amigos(self, user_id):
        rows = self.db.select(
            sentence = "SELECT s1.IDUsuarioSeguido FROM SEGUIDOR AS s1 INNER JOIN SEGUIDOR AS s2 ON s1.IDUsuarioSeguido = s2.IDUsuarioSeguidor WHERE s1.IDUsuarioSeguidor=? AND s2.IDUsuarioSeguido=?",
            parameters = [user_id,user_id]
        )
        resultado = []
        for r in rows:
            resultado.append(self.get_usuario(r["IDUsuarioSeguido"]))

        return resultado
        
    def get_noamigos(self, user_id):
        rows = self.db.select(
            sentence = "SELECT u.IDUsuario, u.Nombre, u.Email, u.Estado, u.IDFavorito FROM Usuario u WHERE u.IDUsuario <> ? AND NOT EXISTS (SELECT 1 FROM SEGUIDOR s WHERE s.IDUsuarioSeguidor = ? AND s.IDUsuarioSeguido = u.IDUsuario) AND NOT EXISTS (SELECT 1 FROM SEGUIDOR s WHERE s.IDUsuarioSeguidor = u.IDUsuario AND s.IDUsuarioSeguido = ?)",
            parameters = [user_id,user_id,user_id]
        )

        return [ dict(row) for row in rows ]
        
    def get_solicitud(self, user_id):
        rows = self.db.select(
            sentence="SELECT u.IDUsuario, u.Nombre, u.Email, u.Estado, u.IDFavorito FROM Usuario u INNER JOIN SEGUIDOR s1 ON s1.IDUsuarioSeguido = u.IDUsuario WHERE s1.IDUsuarioSeguidor = ? AND NOT EXISTS (SELECT 1 FROM SEGUIDOR s2 WHERE s2.IDUsuarioSeguidor = u.IDUsuario AND s2.IDUsuarioSeguido = ?)",
            parameters=[user_id, user_id]
        )

        return [dict(row) for row in rows]
        
    def get_esperandoamigo(self, user_id):
        rows = self.db.select(
            sentence="SELECT u.IDUsuario, u.Nombre, u.Email, u.Estado, u.IDFavorito FROM Usuario u INNER JOIN SEGUIDOR s1 ON s1.IDUsuarioSeguidor = u.IDUsuario WHERE s1.IDUsuarioSeguido = ? AND NOT EXISTS (SELECT 1 FROM SEGUIDOR s2 WHERE s2.IDUsuarioSeguidor = ? AND s2.IDUsuarioSeguido = u.IDUsuario)",
            parameters=[user_id, user_id]
        )

        return [dict(row) for row in rows]
        
#-----------------------------GESTIÓN AMIGOS----------------------------------#

    def dejarseguir(self, ses_id, user_id):
        self.db.delete(
            sentence = "DELETE FROM SEGUIDOR WHERE IDUsuarioSeguidor=? AND IDUsuarioSeguido=?",
            parameters=[ses_id,user_id]
        )
    
    def seguir(self, ses_id, user_id):
        self.db.insert(
            sentence = "INSERT INTO SEGUIDOR VALUES(?,?)",
            parameters = [user_id,ses_id]
        )
        
#------------------------------MANAGE USERS-----------------------------------#
#-----------------------------GETTERS MANAGE----------------------------------#
        
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
        
#-----------------------------BOTONES MANAGE----------------------------------#
        
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
        
#-----------------------------MODIFICAR DATOS----------------------------------#
        
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
            
#--------------------------MODIFICAR DATOS ADMIN-------------------------------#
        
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
        
        
        

class GestorChatBot:
    def __init__(self, gestor_especies, gestor_equipos):
        self.gestor_especies = gestor_especies
        self.gestor_equipos = gestor_equipos

        # comandos soportados y nº de argumentos
        self.comandos = {
            "/stats": 1,
            "/weaknesses": 1,
            "/evolution": 1,
            "/score_team": 1,
            "/compare": 2
        }

    def procesarComando(self, pComando: str) -> str:
        comando = (pComando or "").strip()

        # 1) vacío
        if not comando:
            return "No se puede enviar un mensaje vacío."

        # 2) debe empezar por /
        if not comando.startswith("/"):
            return "Error de sintaxis. Falta el icono de inicio de comando '/'."

        partes = comando.split()
        cmd = partes[0]
        args = partes[1:]
        
        if cmd == "/":
            return "Error de sintaxis. Falta el comando."
        
        # 3) comando existe
        if cmd not in self.comandos:
            return "Error de sintaxis. Comando no encontrado."

        # 4) nº de argumentos correcto
        n_req = self.comandos[cmd]
        if len(args) < n_req:
            return "Error de sintaxis. Falta el argumento."
        if len(args) > n_req:
            # si quieres permitir nombres compuestos, lo vemos luego.
            # ahora, mínimo correcto:
            return "Error de sintaxis. Demasiados argumentos."

        # 5) enrutar
        if cmd == "/stats":
            return self._cmd_stats(args[0])

        if cmd == "/weaknesses":
            return "Comando válido. (weaknesses pendiente de implementar)"

        if cmd == "/evolution":
            return "Comando válido. (evolution pendiente de implementar)"

        if cmd == "/compare":
            return "Comando válido. (compare pendiente de implementar)"

        if cmd == "/score_team":
            return "Comando válido. (score_team pendiente de implementar)"

        return "Error interno."

    # --------- Implementación mínima real (BD) ---------
    def _cmd_stats(self, nombre_pokemon: str) -> str:
        # Buscar pokemon en BD (por nombre)
        p = self.gestor_especies.getPokemonPorNombre(nombre_pokemon)
        if not p:
            return "Pokémon no encontrado."

        # Formato de respuesta simple y claro
        # Campos de la tabla Pokemon: Nombre, Nivel, PS, Ataque, Defensa, AtaqueEspecial, DefensaEspecial, Velocidad
        return (
            f"{p.get('Nombre')} "
            f"(PS {p.get('PS')}, Atq {p.get('Ataque')}, Def {p.get('Defensa')}, "
            f"AtqEsp {p.get('AtaqueEspecial')}, DefEsp {p.get('DefensaEspecial')}, Vel {p.get('Velocidad')})."
        )

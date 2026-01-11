from flask import Blueprint, render_template, request, jsonify
from app.controller.model.GestorChatBot import GestorChatBot
from app.controller.model.GestorEspecies import GestorEspecies
from app.controller.model.GestorEquipos import GestorEquipos


def chatbot_blueprint(db):
    chatbot_bp = Blueprint("chatbot", __name__)

    gestor_especies = GestorEspecies(db)
    gestor_equipos = GestorEquipos(db)
    gestor_chatbot = GestorChatBot(gestor_especies, gestor_equipos)

    @chatbot_bp.route("/chatbot", methods=["GET"])
    def vista_chatbot():
        return render_template("chatbot.html")

    @chatbot_bp.route("/chatbot/consultar", methods=["POST"])
    def consultar_chatbot():
        data = request.get_json(silent=True) or {}
        comando = (data.get("comando") or "").strip()

        respuesta = gestor_chatbot.procesarComando(comando)
        return jsonify({"respuesta": respuesta})

    return chatbot_bp


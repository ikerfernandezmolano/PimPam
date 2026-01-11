from flask import Blueprint, render_template, request, jsonify

def chatbot_blueprint(db):
    chatbot_bp = Blueprint("chatbot", __name__)

    @chatbot_bp.route("/chatbot", methods=["GET"])
    def vista_chatbot():
        return render_template("chatbot.html")

    # TAREA 2: endpoint dummy para recibir comandos
    @chatbot_bp.route("/chatbot/consultar", methods=["POST"])
    def consultar_chatbot():
        data = request.get_json(silent=True) or {}
        comando = (data.get("comando") or "").strip()

        if not comando:
            return jsonify({"respuesta": "No se puede enviar un mensaje vacío."})

        return jsonify({"respuesta": f"OK recibido: {comando}"})

    return chatbot_bp

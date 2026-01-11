from flask import Blueprint, render_template

def chatbot_blueprint(db):
    chatbot_bp = Blueprint("chatbot", __name__)

    @chatbot_bp.route("/chatbot", methods=["GET"])
    def vista_chatbot():
        # TAREA 1: solo mostrar la pantalla (sin lógica todavía)
        return render_template("chatbot.html")

    return chatbot_bp

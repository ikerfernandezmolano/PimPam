<<<<<<< HEAD
=======
from flask import Flask

>>>>>>> master
from app import create_app

app = create_app()

<<<<<<< HEAD
if __name__ == "__main__":
    app.run(debug=True)
=======

if __name__ == '__main__':
    app.run(debug=True)   # para no tener que reiniciar el servidor al hacer pruebas añadir parámetro--> debug=True
>>>>>>> master

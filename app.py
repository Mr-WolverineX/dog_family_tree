from flask import Flask, request, jsonify, render_template
from routes.dogs import dogs_bp
from routes.genealogy import genealogy_bp  # 🔹 Importamos el Blueprint de genealogía
from db import dogs_collection, descendant_requests



app = Flask(__name__)

# 🔹 Registramos los módulos (Blueprints)
app.register_blueprint(dogs_bp)
app.register_blueprint(genealogy_bp)

@app.route("/")
def home():
    return jsonify({"message": "¡La API está funcionando correctamente!"})

@app.route("/insertDog", methods=["GET"])
def show_form():
    return render_template("insertDog.html")  # 🔹 Esto mostrará el formulario en la interfaz

# 📌 Manejo de errores globales
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor", "detalle": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

@app.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    dados = request.json
    nome = dados.get("nome")
    email = dados.get("email")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Usuário cadastrado com sucesso"})

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(usuarios)

@app.route("/")
def home():
    return "API funcionando"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

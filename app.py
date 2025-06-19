from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
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

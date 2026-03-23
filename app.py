from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "agenda_secreta"

# Criar banco
def criar_banco():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        servico TEXT,
        data TEXT,
        hora TEXT
    )
    """)

    conn.commit()
    conn.close()

criar_banco()


# Página inicial
@app.route("/")
def index():
    return render_template("index.html")


# Salvar agendamento
@app.route("/agendar", methods=["POST"])
def agendar():

    nome = request.form["nome"]
    servico = request.form["servico"]
    data = request.form["data"]
    hora = request.form["hora"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agendamentos
        (nome, servico, data, hora)
        VALUES (?, ?, ?, ?)
    """, (nome, servico, data, hora))

    conn.commit()
    conn.close()

    return redirect("/")


# Login admin
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin" and senha == "Julia888":

            session["admin"] = True
            return redirect("/agenda")

    return render_template("login.html")


# Página agenda admin
@app.route("/agenda")
def agenda():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM agendamentos
        ORDER BY data, hora
    """)

    dados = cursor.fetchall()

    conn.close()

    return render_template("agenda.html", dados=dados)


# Cancelar agendamento
@app.route("/cancelar/<int:id>")
def cancelar(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM agendamentos WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/agenda")


# Logout
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
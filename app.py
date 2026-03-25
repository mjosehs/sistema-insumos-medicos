from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "clave_secreta_123"

def get_db():
    return sqlite3.connect("database.db")

def crear_tablas():

    db = get_db()
    cursor = db.cursor()

    # tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entradas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        insumo TEXT,
        cantidad INTEGER,
        fecha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asignaciones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trabajador TEXT,
        insumo TEXT,
        cantidad INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS merma(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        insumo TEXT,
        cantidad INTEGER,
        motivo TEXT
    )
    """)

    db.commit()

    # crear usuario admin por defecto
    password_hash = generate_password_hash("1234")

    try:
        cursor.execute(
            "INSERT INTO usuarios(username,password) VALUES(?,?)",
            ("admin", password_hash)
        )
        db.commit()
    except:
        pass

    db.close()

crear_tablas()

# LOGIN
@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()

        user = cursor.execute(
            "SELECT * FROM usuarios WHERE username=?",
            (username,)
        ).fetchone()

        db.close()

        if user and check_password_hash(user[2], password):

            session["usuario"] = username

            return redirect("/dashboard")

        else:

            return render_template(
                "login.html",
                error="Usuario o contraseña incorrectos"
            )

    return render_template("login.html")

# cerrar sesión
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# proteger acceso
def protegido():

    if "usuario" not in session:

        return False

    return True


@app.route("/dashboard")
def dashboard():

    if not protegido():

        return redirect("/")

    db = get_db()

    cursor = db.cursor()

    entradas = cursor.execute("SELECT * FROM entradas").fetchall()

    return render_template(
        "dashboard.html",
        entradas=entradas,
        usuario=session["usuario"]
    )


@app.route("/entradas", methods=["GET","POST"])
def entradas():

    if not protegido():

        return redirect("/")

    if request.method == "POST":

        insumo = request.form["insumo"]

        cantidad = request.form["cantidad"]

        fecha = request.form["fecha"]

        db = get_db()

        cursor = db.cursor()

        cursor.execute(
        "INSERT INTO entradas(insumo,cantidad,fecha) VALUES(?,?,?)",
        (insumo,cantidad,fecha)
        )

        db.commit()

        db.close()

        return redirect("/dashboard")

    return render_template("entradas.html")


@app.route("/asignacion", methods=["GET","POST"])
def asignacion():

    if not protegido():

        return redirect("/")

    if request.method == "POST":

        trabajador = request.form["trabajador"]

        insumo = request.form["insumo"]

        cantidad = request.form["cantidad"]

        db = get_db()

        cursor = db.cursor()

        cursor.execute(
        "INSERT INTO asignaciones(trabajador,insumo,cantidad) VALUES(?,?,?)",
        (trabajador,insumo,cantidad)
        )

        db.commit()

        db.close()

        return redirect("/reportes")

    return render_template("asignacion.html")


@app.route("/merma", methods=["GET","POST"])
def merma():

    if not protegido():

        return redirect("/")

    if request.method == "POST":

        insumo = request.form["insumo"]

        cantidad = request.form["cantidad"]

        motivo = request.form["motivo"]

        db = get_db()

        cursor = db.cursor()

        cursor.execute(
        "INSERT INTO merma(insumo,cantidad,motivo) VALUES(?,?,?)",
        (insumo,cantidad,motivo)
        )

        db.commit()

        db.close()

        return redirect("/dashboard")

    return render_template("merma.html")


@app.route("/reportes")
def reportes():

    if not protegido():

        return redirect("/")

    db = get_db()

    cursor = db.cursor()

    asignaciones = cursor.execute(
        "SELECT * FROM asignaciones"
    ).fetchall()

    return render_template(
        "reportes.html",
        asignaciones=asignaciones
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5002))

    app.run(host="0.0.0.0", port=port)
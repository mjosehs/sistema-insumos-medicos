from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

def crear_tablas():

    db = get_db()

    cursor = db.cursor()

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
    
@app.route("/merma", methods=["GET","POST"])
def merma():

    if request.method == "POST":

        insumo = request.form["insumo"]
        cantidad = request.form["cantidad"]
        motivo = request.form["motivo"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""

        INSERT INTO merma(insumo,cantidad,motivo)

        VALUES(?,?,?)

        """,(insumo,cantidad,motivo))

        db.commit()

        return redirect("/dashboard")

    return render_template("merma.html")

    db = get_db()
    cursor = db.cursor()

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

    db.commit()

crear_tablas()

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    db = get_db()
    cursor = db.cursor()

    entradas = cursor.execute("SELECT * FROM entradas").fetchall()

    return render_template("dashboard.html", entradas=entradas)

@app.route("/entradas", methods=["GET","POST"])
def entradas():

    if request.method == "POST":

        insumo = request.form["insumo"]
        cantidad = request.form["cantidad"]
        fecha = request.form["fecha"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
        INSERT INTO entradas(insumo,cantidad,fecha)
        VALUES(?,?,?)
        """,(insumo,cantidad,fecha))

        db.commit()

        return redirect("/dashboard")

    return render_template("entradas.html")

@app.route("/asignacion", methods=["GET","POST"])
def asignacion():

    if request.method == "POST":

        trabajador = request.form["trabajador"]
        insumo = request.form["insumo"]
        cantidad = request.form["cantidad"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
        INSERT INTO asignaciones(trabajador,insumo,cantidad)
        VALUES(?,?,?)
        """,(trabajador,insumo,cantidad))

        db.commit()

        return redirect("/reportes")

    return render_template("asignacion.html")

@app.route("/reportes")
def reportes():

    db = get_db()
    cursor = db.cursor()

    asignaciones = cursor.execute("SELECT * FROM asignaciones").fetchall()

    return render_template("reportes.html", asignaciones=asignaciones)

app.run(debug=True, port=5002)
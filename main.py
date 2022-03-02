from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)
cliente = pymongo.MongoClient("mongodb://localhost:27017")
db = cliente['blog']


@app.route("/")
def listado():
    # listar alumnos
    blog = db['entradas']
    resultado = blog.find().sort("fecha", -1).limit(5)

    salida = []
    for x in resultado:
        print(x)
        salida.append(x)

    return render_template("listado.html", entradas=salida)


@app.route("/api/nueva", methods=['GET'])
def nueva_entrada():
    return render_template("formulario.html")


@app.route("/api/nueva", methods=['POST'])
def guardar_entrada():
    # Añadir un nuevo alumno
    titulo = request.form['titulo']
    contenido = request.form['contenido']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']

    blog = db['entradas']
    nueva_entrada = {"titulo": titulo, "contenido": contenido, "descripcion": descripcion, "fecha": fecha}
    blog.insert_one(nueva_entrada)

    return redirect(url_for('listado'))


@app.route("/api/<string:id>", methods=['GET'])
def mostrar_entrada(id):
    blog = db['entradas']
    # Encontrar una entrada
    info = blog.find_one({"_id": ObjectId(id)})
    return render_template("mostrar.html", titulo=info['titulo'], contenido=info['contenido'],
                           descripcion=info['descripcion'], fecha=info['fecha'])


@app.route("/api/modificar/<string:id>", methods=['GET'])
def cambiar_entrada(id):
    blog = db['entradas']
    # Encontrar una entrada
    info = blog.find_one({"_id": ObjectId(id)})
    return render_template("modificar.html", titulo=info['titulo'], contenido=info['contenido'],
                           descripcion=info['descripcion'], fecha=info['fecha'])


app.run()

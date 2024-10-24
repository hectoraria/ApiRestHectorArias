from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utilidad.functions import *

rutaActores = "ficheros/actores.json"
rutaPeliculas = "ficheros/pelicula.json"
actoresBP = Blueprint('actores', __name__)

@actoresBP.get('/')
def getActores():
    actores = leeFichero(rutaActores)
    return jsonify(actores), 200

@actoresBP.post('/')
def addActor():
    actores = leeFichero(rutaActores)
    peliculas = leeFichero(rutaPeliculas)
    if request.is_json:
        nuevoActor = request.get_json()
        for pelicula in peliculas:
            if pelicula["id"] == nuevoActor["id_pelicula"]:
                nuevoActor["id"] = nuevo_id(actores)
                actores.append(nuevoActor)
                escribeFichero(actores, rutaActores)
                return nuevoActor, 201
        return {"error": "película no encontrada"}, 404
    else:
        return {"error": "JSON no es correcto"}, 415


@actoresBP.delete('/<int:id>')
@jwt_required()
def borraActor(id):
    listaActores = leeFichero(rutaActores)
    for actor in listaActores:
        if actor["id"] == id:
            listaActores.remove(actor)
            escribeFichero(listaActores, rutaActores)
            return {}, 200
    return {"error": "actor no encontrado"}, 404
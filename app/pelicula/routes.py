from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utilidad.functions import *

peliculasBP = Blueprint('pelicula', __name__)
rutaPeliculas = "ficheros/peliculas.json"
rutaActores = "ficheros/actores.json"

@peliculasBP.get('/<int:id_pelicula>')
def getPelicula(id_pelicula):
    peliculas = leeFichero(rutaPeliculas)
    for pelicula in peliculas:
        if pelicula["id"] == id_pelicula:
            return pelicula, 200
    return {"error" : "Película no encontrada"}, 404

@peliculasBP.get('/<int:id_pelicula>/actores')
def getActores(id_pelicula):
    actores = leeFichero(rutaActores)
    lista = []
    for actor in actores:
        if actor["id_pelicula"] == id_pelicula:
            lista.append(actor)
    if len(lista) > 0:
        return lista, 200
    return {"error": "no hay actores para la película indicada"}, 404

@peliculasBP.put('/<int:id_pelicula>')
@jwt_required()
def modificaPelicula(id_pelicula):
    peliculas = leeFichero(rutaPeliculas)
    if request.is_json:
        nueva_pelicula = request.get_json()
        for pelicula in peliculas:
            if pelicula["id"] == id_pelicula:
                pelicula.update(nueva_pelicula)
                escribeFichero(peliculas, rutaPeliculas)
                return pelicula, 200
        nueva_pelicula["id"] = id_pelicula
        peliculas.append(nueva_pelicula)
        escribeFichero(peliculas, rutaPeliculas)
        return nueva_pelicula, 201
    else:
        return {"error": "JSON erróneo"}, 415

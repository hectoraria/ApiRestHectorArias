from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utilidad.functions import *

rutaDirectores = "ficheros/directores.json"
rutaSupermercados = "ficheros/supermercados.json"

directoresBP = Blueprint('directores', __name__)

@directoresBP.get('/')
def getDirector():
    directores = leeFichero(rutaDirectores)
    return jsonify(directores), 200

@directoresBP.post('/')
def addActor():
    directores = leeFichero(rutaDirectores)
    supermercados = leeFichero(rutaSupermercados)
    if request.is_json:
        nuevoDirector = request.get_json()
        for pelicula in supermercados:
            if pelicula["id"] == nuevoDirector["id_supermercado"]:
                nuevoDirector["id"] = nuevo_id(directores)
                directores.append(nuevoDirector)
                escribeFichero(directores, rutaDirectores)
                return nuevoDirector, 201
        return {"error": "Super no encontrada"}, 404
    else:
        return {"error": "JSON no es correcto"}, 415


@directoresBP.delete('/<int:id>')
@jwt_required()
def borraDirector(id):
    listaDirectores = leeFichero(rutaDirectores)
    for director in listaDirectores:
        if director["id"] == id:
            listaDirectores.remove(director)
            escribeFichero(listaDirectores, rutaDirectores)
            return {}, 200
    return {"error": "actor no encontrado"}, 404
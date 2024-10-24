from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utilidad.functions import *

supermercadosBP = Blueprint('supermercados', __name__)
rutaSupermecados = "ficheros/supermercados.json"
rutaDirectores = "ficheros/directores.json"



@supermercadosBP.get('/<int:id_supermercado>')
def getSupermercado(id_supermercado):
    supermercados = leeFichero(rutaSupermecados)
    for super in supermercados:
        if super["id"] == id_supermercado:
            return super, 200
    return {"error" : "Película no encontrada"}, 404

@supermercadosBP.get('/<int:id_supermercado>/directores')
def getActores(id_supermercado):
    directores = leeFichero(rutaDirectores)
    lista = []
    for dire in directores:
        if dire["id_supermercado"] == id_supermercado:
            lista.append(dire)
    if len(lista) > 0:
        return lista, 200
    return {"error": "no hay directores para la película indicada"}, 404

@supermercadosBP.put('/<int:id_supermercado>')
@jwt_required()
def modificaPelicula(id_supermercado):
    supermercados = leeFichero(rutaSupermecados)
    if request.is_json:
        nuevo_supermercado = request.get_json()
        for super in supermercados:
            if super["id"] == id_supermercado:
                super.update(nuevo_supermercado)
                escribeFichero(supermercados, rutaSupermecados)
                return super, 200
        nuevo_supermercado["id"] = id_supermercado
        supermercados.append(nuevo_supermercado)
        escribeFichero(supermercados, rutaSupermecados)
        return nuevo_supermercado, 201
    else:
        return {"error": "JSON erróneo"}, 415

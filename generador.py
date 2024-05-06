import json
import pymongo
import pyqrcode
from datadb import *
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])

def generator():
    # Conectar a la base de datos de MongoDB
    client = pymongo.MongoClient(cliente)
    db = client[bd]
    collection = db[coleccion]

    # Obtener el documento con ObjectId "x"
    document = collection.find_one({"_id": ObjectId('x')})

    # Crear un diccionario con los campos que deseas incluir en el código QR
    qr_data = {
        "_id": str(document["_id"]),
        "name": document["name"],
        "stock": 20  # Introducir el valor de stock manualmente
    }

    # Convertir el diccionario a una cadena JSON
    qr_string = json.dumps(qr_data)

    # Generar el código QR
    qr_code = pyqrcode.create(qr_string)

    #Extraer valor del ID del objeto
    qr_name= qr_data.get("ObjectId")

    # Guardar el código QR como imagen PNG
    qr_code.png(qr_name+".png", scale=6)




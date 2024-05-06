import json
import datetime
import pyqrcode
from flask import Flask, request, send_file
from datadb import *

app = Flask(__name__)

@app.route("/generator", methods=['GET'])
def generator():
    # Obtener los argumentos de la URL
    qr_data = {
        "ObjectId": request.args.get('id'),
        "nombre": request.args.get('name'),
        "stock": request.args.get('stock'),
        "color": request.args.get('color'),
        "talla": request.args.get('size') 
    }
    
    # Convertir el diccionario a una cadena JSON
    qr_string = json.dumps(qr_data)

    # Generar el código QR
    qr_code = pyqrcode.create(qr_string)

    #Extraer valor del ID del objeto
    qr_name = qr_data.get("ObjectId")

    # Guardar el código QR como imagen PNG
    png_name = qr_name + datetime.datetime.today().strftime('_%Y%m%d%H%M%S') + ".png"
    qr_code.png(png_name, scale=6)

    return send_file(png_name, mimetype='image/png')

if __name__ == "__main__":
    # Ejecutar la aplicación Flask con los argumentos pasados por la línea de comandos
    app.run(host='127.0.0.1', port=5000, debug=True)

# Importamos las librerías necesarias
import json
import datetime
import pyqrcode
import os
from flask import Flask, request, send_file
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sinc_stock"]

@app.route("/generator_qr", methods=['GET'])
def generator_qr():
    # Obtener los argumentos de la URL
    product_name = request.args.get('name')
    requested_stock = int(request.args.get('stock'))

    # Verificar si el producto existe en la base de datos
    product = db.products.find_one({"name": product_name})
    if not product:
        return "\n \nEl producto no existe en la base de datos.", 404

    # Buscar el stock disponible para el tamaño y color específicos
    stock_available = 0
    for variant in product['variants']:
        if variant['size'] == request.args.get('size') and variant['color'] == request.args.get('color'):
            stock_available = variant['stock']
            break

    # Validar que el stock solicitado sea menor o igual al stock disponible
    if requested_stock > stock_available:
        return f"\n \nEl stock solicitado ({requested_stock}) es mayor que el stock disponible ({stock_available}).",400

    # Convertir los datos del producto a una cadena JSON
    qr_data = {
        "name": product_name,
        "stock": requested_stock,
        "color": request.args.get('color'),
        "size": request.args.get('size')
    }
    qr_string = json.dumps(qr_data)

    # Generar el código QR
    qr_code = pyqrcode.create(qr_string)

    # Obtener el directorio del script actual
    script_dir = os.path.dirname(__file__)

    # Construir la ruta completa del archivo PNG en el mismo directorio que el script
    png_name = os.path.join(script_dir, f"{product_name}_{datetime.datetime.today().strftime('%Y%m%d%H%M%S')}.png")
    qr_code.png(png_name, scale=6)

    response = send_file(png_name, mimetype='image/png')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

# Inicializamos el servidor
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

exit

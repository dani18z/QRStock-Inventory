import json
import os
import datetime
import pyqrcode
from flask import Flask, request, send_file, Response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/docs'  # URL para accder a Swagger UI 
API_URL = '/static/swagger.yaml'  # Nuestra API url 


# Llama a la función de fábrica para crear nuestro blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)
app.register_blueprint(swaggerui_blueprint)


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
        return f"\n \nEl stock solicitado ({requested_stock}) es mayor que el stock disponible ({stock_available}).", 400

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

@app.route("/query_stock", methods=['GET'])
def query_stock():
    # Obtener el nombre del producto de la consulta
    product_name = request.args.get('name')
    size = request.args.get('size')
    color = request.args.get('color')

    # Buscar el producto en la base de datos
    product = db.products.find_one({"name": product_name})

    if product:
        if size and color:
            # Buscar la variante específica por talla y color
            variant = next((v for v in product["variants"] if v["size"] == size and v["color"] == color), None)
            if variant:
                stock = str(variant["stock"])
                return "Stock de " + product_name + " de talla " + size + " y color " + color + ": " +stock 
            else:
                return "No se encontró la variante especificada para " + product_name, 404
        else:
            # Devolver stock de todas las variantes si no se especifica talla y color
            stock_total = str(product.get("totalStock", "No disponible"))
            return "Stock total de " + product_name + ": " + stock_total, 200
    else:
        return "El producto " + product_name + " no fue encontrado en la base de datos.", 404

@app.route("/sum_stock", methods=['POST'])
def sum_stock():
    # Obtener el contenido del código QR desde la solicitud
    qr_content = request.get_json()

    # Obtener el nombre del producto del código QR
    product_name = qr_content.get('name')

    # Buscar el producto en la base de datos
    product = db.products.find_one({"name": product_name})

    if product:
        # Actualizar el stock del producto para la talla y color respectivos
        size = qr_content.get('size')
        color = qr_content.get('color')
        stock_change = int(qr_content.get('stock'))  # Cantidad a cambiar en el stock

        for variant in product['variants']:
            if variant['size'] == size and variant['color'] == color:
                # Actualizar el stock de la variante
                variant['stock'] += stock_change
                
                # Actualizar el totalStock del producto
                product['totalStock'] += stock_change
                
                # Actualizar el documento en la base de datos
                db.products.update_one({"_id": product["_id"]}, {"$set": {"variants": product['variants'], "totalStock": product['totalStock']}})
                return "\n \n Stock actualizado correctamente.",200
        
        return "\n \n No se encontró una variante correspondiente para actualizar el stock.",404
    else:
        return "\n \n Producto no encontrado en la base de datos.",404

@app.route("/subtract_stock", methods=['POST'])
def subtract_stock():
    # Obtener el contenido del código QR desde la solicitud
    qr_content = request.get_json()

    # Obtener el nombre del producto del código QR
    product_name = qr_content.get('name')

    # Buscar el producto en la base de datos
    product = db.products.find_one({"name": product_name})

    if product:
        # Actualizar el stock del producto para la talla y color respectivos
        size = qr_content.get('size')
        color = qr_content.get('color')
        stock_change = int(qr_content.get('stock'))  # Cantidad a cambiar en el stock

        for variant in product['variants']:
            if variant['size'] == size and variant['color'] == color:
                
                # Actualizar el stock de la variante
                variant['stock'] -= stock_change
                
                # Actualizar el totalStock del producto
                product['totalStock'] -= stock_change
                
                # Actualizar el documento en la base de datos
                db.products.update_one({"_id": product["_id"]}, {"$set": {"variants": product['variants'], "totalStock": product['totalStock']}})
                return "\n \n Stock actualizado correctamente.",200
        
        return "\n \n No se encontró una variante correspondiente para actualizar el stock.",404
    else:
        return "\n \n Producto no encontrado en la base de datos.",404

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

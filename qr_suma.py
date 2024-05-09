import json
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sinc_stock"]

@app.route("/qr_suma", methods=['POST'])
def qr_suma():
    # Obtener el contenido del código QR desde la solicitud
    qr_content = request.get_json()

    # Obtener el nombre del producto del código QR
    product_name = qr_content.get('name')

    # Buscar el producto en la base de datos
    product = db.inventory.find_one({"name": product_name})

    if product:
        # Actualizar el stock del producto para la talla y color respectivos
        size = qr_content.get('size')
        color = qr_content.get('color')
        stock = int(qr_content.get('stock'))

        for variant in product['variants']:
            if variant['size'] == size and variant['color'] == color:
                variant['stock'] += stock
                db.inventory.update_one({"_id": product["_id"]}, {"$set": {"variants": product['variants']}})
                return "\n \n Stock actualizado correctamente."
        
        return "\n \n No se encontró una variante correspondiente para actualizar el stock."
    else:
        return "\n \n Producto no encontrado en la base de datos."

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

import json
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sinc_stock"]

@app.route("/qr_resta", methods=['POST'])
def qr_resta():
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
        stock_change = int(qr_content.get('stock'))  # Cantidad a cambiar en el stock

        for variant in product['variants']:
            if variant['size'] == size and variant['color'] == color:
                
                # Actualizar el stock de la variante
                variant['stock'] -= stock_change
                
                # Actualizar el totalStock del producto
                product['totalStock'] -= stock_change
                
                # Actualizar el documento en la base de datos
                db.inventory.update_one({"_id": product["_id"]}, {"$set": {"variants": product['variants'], "totalStock": product['totalStock']}})
                return "\n \n Stock actualizado correctamente."
        
        return "\n \n No se encontró una variante correspondiente para actualizar el stock."
    else:
        return "\n \n Producto no encontrado en la base de datos."

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

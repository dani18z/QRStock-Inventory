from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sinc_stock"]

# Función para permitir solicitudes desde cualquier origen
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

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
                stock = variant["stock"]
                return jsonify({"product": product_name, "size": size, "color": color, "stock": stock})
            else:
                return jsonify({"error": "No se encontró la variante especificada para el producto '{}'.".format(product_name)}), 404
        else:
            # Devolver stock de todas las variantes si no se especifica talla y color
            stock_variants = [{"size": v["size"], "color": v["color"], "stock": v["stock"]} for v in product["variants"]]
            return jsonify({"product": product_name, "stock_variants": stock_variants})
    else:
        return jsonify({"error": "El producto '{}' no fue encontrado en la base de datos.".format(product_name)}), 404

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

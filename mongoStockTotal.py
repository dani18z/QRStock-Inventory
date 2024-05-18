from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sinc_stock"]

# Agregar la etapa de agregación para calcular la suma del stock total por documento
pipeline = [
    {"$project": {
        "_id": 1,  # Mantener el ID original del documento
        "name": 1,  # Mantener el nombre del producto
        "price": 1,  # Mantener el precio del producto
        "category": 1,  # Mantener la categoría del producto
        "variants": 1,  # Mantener la lista de variantes del producto
        "stock_total": {"$sum": "$variants.stock"}  # Calcular la suma del stock de todas las variantes
    }}
]

# Ejecutar la agregación y actualizar los documentos en la colección con el stock total calculado
result = db.inventory.aggregate(pipeline)
for item in result:
    db.inventory.update_one({"_id": item["_id"]}, {"$set": {"stock_total": item["stock_total"]}})

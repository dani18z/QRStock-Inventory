import pymongo
import pyqrcode
from pyzbar import pyzbar
import cv2
from datadb import *

# Conectar a la base de datos de MongoDB
client = pymongo.MongoClient(cliente)
db = client[coleccion]
collection = db[coleccion]

# Leer el QR code desde una imagen o desde la cámara web
def read_qr(image_path=None):
    if image_path:
        img = cv2.imread(image_path)
    else:
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        cap.release()

    decoded_objects = pyzbar.decode(img)
    for obj in decoded_objects:
        qr_data = obj.data.decode("utf-8")
        return qr_data

# Leer el QR code
qr_data = read_qr()   #Omitir el parámetro "documento_qr.png" para leer desde la cámara web

# Parsear el diccionario desde la cadena del QR code
qr_dict = eval(qr_data)

# Obtener el documento actual en la base de datos
document_id = ObjectId(qr_dict["_id"])
document = collection.find_one({"_id": document_id})

# Sumar el stock del QR al stock actual en la base de datos
new_stock = document["stock"] + qr_dict["stock"]

# Actualizar el documento en la base de datos
collection.update_one({"_id": document_id}, {"$set": {"stock": new_stock}})

print("Documento actualizado correctamente!")
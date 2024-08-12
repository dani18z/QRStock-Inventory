import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["almacen_01"]

col_products = db["products"]
col_users = db["users"]

with open("products.json") as f:  
  products_data = json.load(f)  
x = col_products.insert_many(products_data)

with open("users.json") as f:  
  users_data = json.load(f)  
y = col_users.insert_many(users_data)


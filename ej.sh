
#cURL Generador qr
curl -X GET "http://127.0.0.1:5000/generator_qr?name=CamisaMangaCorta&stock=50&color=Blanco&size=S"

#cURL Consulta stock
curl -X GET "http://127.0.0.1:5000/query_stock?name=CamisaMangaCorta&size=M&color=Blanco"

#cURL Suma stock
curl -X POST "http://127.0.0.1:5000/sum_stock" -H "Content-Type: application/json" -d "{"name": "CamisaMangaCorta", "size": "S", "color": "Blanco", "stock": "50"}" 

#cURL Resta stock
curl -X POST "http://127.0.0.1:5000/subtraction_stock" -H "Content-Type: application/json" -d "{"name": "CamisaMangaCorta", "size": "S", "color": "Blanco", "stock": "20"}" 



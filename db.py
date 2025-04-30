import os
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("mongo_uri")  # 🔹 Ahora sí carga la URI desde .env

client = MongoClient(mongo_uri, tlsCAFile=certifi.where())  # 🔹 Conexión segura
db = client["dog_family_tree"]  # 🔹 Base de datos
dogs_collection = db["dogs"]
descendant_requests = db["descendant_requests"]



#from pymongo import MongoClient
#
## 🔹 Conexión a MongoDB
#client = MongoClient("mongo_uri")
#db = client.dog_family_tree  # Base de datos específica del proyecto
#
## 🔹 Colecciones importantes
#dogs_collection = db["dogs"]
#descendant_requests = db["descendant_requests"]




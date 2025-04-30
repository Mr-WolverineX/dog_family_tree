from flask import Blueprint, request, jsonify
from db import dogs_collection
from models import validate_data
from db import dogs_collection, descendant_requests

from bson import ObjectId

dogs_bp = Blueprint("dogs", __name__)


# 🔹 Endpoint para obtener informacion de un perro por su ID
from bson import ObjectId

@dogs_bp.route("/dogs/<dog_id>", methods=["GET"])
def get_dog(dog_id):
    """Busca un perro en la base de datos por su ID y devuelve su información"""
    try:
        # 🔹 Validación del ID antes de convertirlo a ObjectId
        if not dog_id or not ObjectId.is_valid(dog_id):
            return jsonify({"error": "Formato de ID inválido"}), 400

        dog = dogs_collection.find_one({"_id": ObjectId(dog_id)})
        if not dog:
            return jsonify({"error": "Perro no encontrado"}), 404

        # 🔹 Convertimos `_id` y cualquier otro ObjectId a string
        dog["_id"] = str(dog["_id"])
        for key, value in dog.items():
            if isinstance(value, ObjectId):
                dog[key] = str(value)        

        return jsonify(dog)
    
    except Exception as e:
        return jsonify({"error": "Error interno", "detalle": str(e)}), 500


@dogs_bp.route("/dogs/name/<dog_name>", methods=["GET"])
def get_dog_by_name(dog_name):
    """Busca un perro por nombre y devuelve su información con padres y descendencia"""
    #dog = dogs_collection.find_one({"name": dog_name})
    dog = dogs_collection.find_one({"name": {"$regex": f"^{dog_name}$", "$options": "i"}})

    if not dog:
        return jsonify({"error": "No se encontró ningún perro con ese nombre"}), 404

    dog["_id"] = str(dog["_id"])  # Convertir ObjectId a string

    # 🔹 Buscar padres
    dog["father"] = dogs_collection.find_one({"_id": ObjectId(dog["father"])}, {"name": 1, "photo": 1}) if dog["father"] else None
    dog["mother"] = dogs_collection.find_one({"_id": ObjectId(dog["mother"])}, {"name": 1, "photo": 1}) if dog["mother"] else None

    # 🔹 Buscar descendientes
    #dog["descendants"] = list(dogs_collection.find({"_id": {"$in": dog["descendants"]}}, {"name": 1, "photo": 1}))
    
    # 📌 Validar si `descendants` es una lista antes de hacer la consulta
    descendant_ids = dog.get("descendants", [])
    if isinstance(descendant_ids, list) and descendant_ids:
        dog["descendants"] = list(dogs_collection.find({"_id": {"$in": descendant_ids}}, {"name": 1, "photo": 1}))
    else:
        dog["descendants"] = []

    return jsonify(dog)




@dogs_bp.route("/dogs/suggestions", methods=["GET"])
def get_dog_suggestions():
    query = request.args.get("name", "").strip()

    if not query:
        return jsonify({"error": "Debe ingresar al menos una letra para buscar"}), 400

    try:
        dogs = list(dogs_collection.find(
            {"name": {"$regex": f"^{query}", "$options": "i"}},
            {"_id": 1, "name": 1, "photo": 1}  # 📌 Incluir foto en la respuesta
        ))
        # 📌 Convertir `_id` a string para evitar problemas en JSON
        for dog in dogs:
            dog["_id"] = str(dog["_id"])

        return jsonify(dogs)

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500




@dogs_bp.route("/dogs", methods=["POST"])
def add_dog():
    """Registra un perro en la base de datos después de validar los datos."""
    data = request.json
    print("Datos recibidos en la solicitud:", data)  # 📌 Ver los datos en la consola de Flask

    # 📌 Validar datos antes de continuar
    errors = validate_data(data)
    if errors:
        return jsonify({"error": "Datos inválidos", "detalles": errors}), 400

    # 📌 Verificar si el perro ya existe por nombre
    existing_dog = dogs_collection.find_one({"name": data["name"]})
    if existing_dog:
        return jsonify({"error": "Ya existe un perro con ese nombre"}), 400

    # 📌 Validación de padres en MongoDB
    parent_ids = []
    father_id = data.get("father")
    mother_id = data.get("mother")

    if father_id and ObjectId.is_valid(father_id):
        parent_ids.append(ObjectId(father_id))
    elif father_id:
        return jsonify({"error": f"El padre con ID {father_id} no es válido"}), 400

    if mother_id and ObjectId.is_valid(mother_id):
        parent_ids.append(ObjectId(mother_id))
    elif mother_id:
        return jsonify({"error": f"La madre con ID {mother_id} no es válida"}), 400

    # 📌 Crear estructura de solicitud en `descendant_requests`
    new_dog = {
        "parent_ids": parent_ids,  # 📌 Solo agregamos IDs válidos
        "descendant": [{
            "name": data["name"],
            "dob": data["dob"],
            "gender": data["gender"],
            "breed": data.get("breed", "Desconocido"),
            "photo": data.get("photo", ""),
            "status": "pendiente"  # 📌 Queda como solicitud hasta aprobación
        }]
    }

    descendant_requests.insert_one(new_dog)
    return jsonify({"message": "Solicitud de registro enviada para aprobación"}), 201




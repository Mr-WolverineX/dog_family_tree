from flask import Blueprint, request, jsonify
from db import dogs_collection, descendant_requests
from bson import ObjectId

genealogy_bp = Blueprint("genealogy", __name__)  # Modularizamos genealogía en un Blueprint

# 🔹 Solicitar agregar un descendiente
@genealogy_bp.route("/dogs/<dog_id>/request-descendant", methods=["POST"])
def request_descendant(dog_id):
    """Registra una solicitud de descendencia sin modificar la base de datos directamente."""
    data = request.json
    
    # Verificar si el descendiente existe en la BD antes de crear la solicitud
    if not dogs_collection.find_one({"_id": ObjectId(data["descendant_id"])}):
        return jsonify({"error": "El descendiente no existe"}), 400

    new_descendant = {"descendant_id": ObjectId(data["descendant_id"]), "status": "pendiente"}

    # Guardamos la solicitud en la colección correspondiente
    #descendant_requests.insert_one({"parent_id": ObjectId(dog_id), "descendant": new_descendant}) # guarda cada solisitud y sobrescribe 
    descendant_requests.update_one(
    {"parent_id": ObjectId(dog_id)},  # 📌 Si ya existe el documento, lo actualiza
    {"$push": {"descendant": {
        "descendant_id": ObjectId(data["descendant_id"]),
        "status": "pendiente"
    }}},  
    upsert=True  # 📌 Esto asegura que si no existe el documento, se cree automáticamente
)


    return jsonify({"message": "Solicitud de descendencia enviada para aprobación"}), 201


# 🔹 Obtener solicitudes pendientes de descendencia
@genealogy_bp.route("/dogs/<dog_id>/pending-descendants", methods=["GET"])
def pending_descendants(dog_id):
    """Lista todas las solicitudes de descendencia pendientes para un perro."""
    requests = list(descendant_requests.find({"parent_ids": {"$in": [ObjectId(dog_id)]}}, {"_id": 0}))

    print("Solicitudes encontradas:", requests)  # 📌 Verifica lo que devuelve la consulta antes de procesar

    formatted_requests = []
    for request in requests:
        if "parent_ids" in request:  # 📌 Asegurarse de que el campo existe antes de modificarlo
            request["parent_ids"] = [str(pid) for pid in request["parent_ids"]]  # 🔹 Corrección

        # 📌 Si `descendant` es una lista, recorrer los elementos correctamente
        if "descendant" in request and isinstance(request["descendant"], list):
            for descendant in request["descendant"]:
                if "descendant_id" in descendant:
                    descendant["descendant_id"] = str(descendant["descendant_id"])

        formatted_requests.append(request)

    return jsonify(formatted_requests)




# 🔹 Aprobar  solicitud una solicitud de descendencia
@genealogy_bp.route("/dogs/<dog_id>/approve-descendant", methods=["PATCH"])
def approve_descendant(dog_id):
    """Aprueba la solicitud y agrega el descendiente a la genealogía."""
    try:
        data = request.json
        descendant_id = ObjectId(data["descendant_id"])

        request_doc = descendant_requests.find_one({"parent_id": ObjectId(dog_id)})
        if not request_doc:
            return jsonify({"error": "Solicitud no encontrada"}), 404

        # 📌 Verificar si `descendant_id` existe dentro de la lista
        found_descendant = next(
            (d for d in request_doc["descendant"] if d["descendant_id"] == descendant_id),
    None
)

        if not found_descendant:
            return jsonify({"error": "Descendiente no encontrado en la solicitud"}), 404

        if found_descendant["status"] != "pendiente":
            return jsonify({"error": "Solicitud ya procesada"}), 400






        # 📌 Mover el perro de `descendant_requests` a `dogs_collection`
        new_dog = request_doc["descendant"]
        new_dog["father"] = ObjectId(dog_id)
        new_dog["descendants"] = []
       

        # Agregamos el descendiente a la lista en MongoDB
        dogs_collection.update_one(
            {"_id": ObjectId(dog_id)},
            {"$push": {"descendants": descendant_id}}  # 📌 Se mantiene como ObjectId
        )

        # Eliminamos la solicitud aprobada
        descendant_requests.update_one(
            {"parent_id": ObjectId(dog_id)},
            {"$pull": {"descendant": {"descendant_id": descendant_id}}}
        )


        return jsonify({"message": "Descendencia aprobada y registrada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": "Error interno en el servidor", "detalle": str(e)}), 500


# 🔹 Rechazar una solicitud de descendencia
@genealogy_bp.route("/dogs/<dog_id>/reject-descendant", methods=["DELETE"])
def reject_descendant(dog_id):
    """Permite a los dueños rechazar una solicitud de descendencia."""
    data = request.json
    descendant_id = ObjectId(data["descendant_id"])

    # 📌 Eliminar el descendiente específico dentro del array
    descendant_requests.update_one(
        {"parent_id": ObjectId(dog_id)},
        {"$pull": {"descendant": {"descendant_id": descendant_id}}}
    )

    # 📌 Si después de eliminar, el documento no tiene más descendientes, eliminarlo completamente
    descendant_requests.delete_one({"parent_id": ObjectId(dog_id), "descendant": {"$size": 0}})

    return jsonify({"message": "Solicitud de descendencia rechazada"}), 200






@genealogy_bp.route("/dogs/genealogy/<dog_id>", methods=["GET"])
def get_genealogy(dog_id):
    """Consulta la genealogía de un perro incluyendo padres y descendientes"""
    dog = dogs_collection.find_one({"_id": ObjectId(dog_id)})

    if not dog:
        return jsonify({"error": "Perro no encontrado"}), 404

    dog["_id"] = str(dog["_id"])
    
    # 📌 Validar padre y madre antes de buscar en la BD
    dog["father"] = dogs_collection.find_one(
        {"_id": ObjectId(dog["father"])} if dog.get("father") and ObjectId.is_valid(dog["father"]) else None,
        {"name": 1, "photo": 1}
    )
    dog["mother"] = dogs_collection.find_one(
        {"_id": ObjectId(dog["mother"])} if dog.get("mother") and ObjectId.is_valid(dog["mother"]) else None,
        {"name": 1, "photo": 1}
    )

    # 📌 Validar si `descendants` es una lista antes de hacer la consulta
    descendant_ids = dog.get("descendants", [])
    if isinstance(descendant_ids, list) and descendant_ids:
        dog["descendants"] = list(dogs_collection.find({"_id": {"$in": descendant_ids}}, {"name": 1, "photo": 1}))
    else:
        dog["descendants"] = []

    return jsonify(dog)





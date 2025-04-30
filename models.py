# 🔹 Definimos la estructura de datos para los perros
schema = {
    "name": {"type": "string", "required": True},
    "dob": {"type": "string", "required": True},
    "gender": {"type": "string", "required": True, "allowed": ["Macho", "Hembra"]},
    "breed": {"type": "string", "required": False},
    "photo": {"type": "string", "required": False},
    "father": {"type": "string", "default": ""},
    "mother": {"type": "string", "default": ""},
    "descendants": {"type": "list", "default": []}
}

# 🔹 Función de validación de datos
def validate_data(data):
    errors = {}
    for key, rules in schema.items():
        if rules.get("required") and key not in data:
            errors[key] = "Este campo es obligatorio."
        elif "allowed" in rules and data.get(key) and data.get(key) not in rules["allowed"]:
            errors[key] = f"Valor no permitido. Opciones válidas: {rules['allowed']}"
        elif key == "descendants" and not isinstance(data.get(key, []), list):
            errors[key] = "Debe ser una lista válida."
    return errors if errors else None

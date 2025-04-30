# 🐶 Dog Family Tree API  
Este proyecto permite registrar perros, visualizar su genealogía y gestionar su información con Flask y MongoDB Atlas.  

## 📌 Estructura del proyecto
dog_family_tree/ 
├── static/ 
│ ├── js/ → 📌 Contiene los scripts de frontend 
│   ├── formHandler.js  → 📌 Captura y validación de datos del formulario
│   ├── apiRequests.js  → 📌 Funciones para enviar datos a Flask con `fetch()`
│   ├── suggestions.js  → 📌 Lógica para buscar padres/madres dinámicamente
│   ├── insertDog.js  → 📌 Archivo principal que conecta todo
│   ├── insertDog.js → 📌 Manejo de inserción de perros desde la web 
│ ├── css/ → 📌 Estilos del frontend 

├── templates/ 
│ ├── insertDog.html → 📌 Formulario HTML para registrar perros 

├── routes/ 
│ ├── dogs.py → 📌 Endpoints generales (registro, búsqueda) 
│ ├── genealogy.py → 📌 Árbol genealógico (padres, descendientes) 

├── app.py → 📌 Archivo principal que ejecuta Flask 
├── db.py → 📌 Configuración de conexión con MongoDB Atlas 
├── models.py  → 📌 Definicion de estructura y validacion de datos
├── Markdown.md → 📌 Documentación del proyecto



## 🚀 Instalación
Para ejecutar este proyecto, sigue estos pasos:  
1️⃣ **Clona el repositorio:**  
```bash
git clone https://github.com/tu_usuario/dog_family_tree.git
cd dog_family_tree


## Instalacion de dependencias
pip install -r requirements.txt



🔥 Uso de la API
La API tiene los siguientes endpoints:

Método	    Endpoint	                        Descripción
POST	    /dogs	                            Registra un nuevo perro en la base de datos

GET	        /dogs/name/<nombre>	                Busca un perro por nombre

GET	        /dogs/genealogy/<id>                Obtiene el árbol genealógico de un perro

GET	       /dogs/suggestions?name=<texto>	    Devuelve sugerencias de nombres de perros


## Ejemplo de solicitud para registrar perros
{
  "name": "Luna",
  "breed": "Pomeranian",
  "dob": "2020-04-15",
  "gender": "Hembra",
  "photo": "https://perro.shop/wp-content/uploads/pomeranian.jpg",
  "father": "67f8cabb6c05eaee5bcfc6ae",
  "mother": "67f8cabb6c05eaee5bcfc6af",
  "descendants": ["67f8cabb6c05eaee5bcfc6b0"]
}

📌 Contacto
Si tienes dudas o mejoras para el código, puedes contactar a Alexander en su repositorio de GitHub. 🚀

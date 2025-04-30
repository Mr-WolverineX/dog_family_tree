export function fetchDogSuggestions(query, parentType) {
    const suggestionsBox = document.getElementById(`${parentType}Suggestions`);

    // 📌 Si el campo está vacío, limpiar la lista antes de cualquier condición
    if (query.trim() === "") {
        suggestionsBox.innerHTML = "";
        return;
    }
    
    // 📌 Si hay menos de 2 caracteres, no buscar
    if (query.length < 2) return;

    fetch(`/dogs/suggestions?name=${query}`)
        .then(response => response.json())
        .then(data => {
            suggestionsBox.innerHTML = ""; // 📌 Limpiar lista anterior

            data.forEach(dog => {
                const listItem = document.createElement("li");
                listItem.classList.add("suggestion-item");

                // 📌 Crear imagen pequeña
                const img = document.createElement("img");
                img.src = dog.photo;
                img.alt = dog.name;
                img.classList.add("suggestion-img");

                // 📌 Establecer el tamaño directamente en los atributos HTML
                img.setAttribute("width", "40");
                img.setAttribute("height", "40");

                // 📌 Crear texto con el nombre
                const span = document.createElement("span");
                span.textContent = dog.name;

                // 📌 Agregar imagen y nombre al elemento de la lista
                listItem.appendChild(img);
                listItem.appendChild(span);
                listItem.onclick = () => {
                    console.log(`Seleccionando padre/madre: ${dog.name}, ID: ${dog._id}`); // 📌 Verificar los valores
                    if (dog._id) {
                        document.getElementById(parentType).value = dog.name; // 📌 Muestra el nombre seleccionado
                        document.getElementById(parentType).setAttribute("data-id", dog._id); // 📌 Guarda el ID correctamente
                        console.log(`ID almacenado para ${parentType}:`, document.getElementById(parentType).getAttribute("data-id")); // 📌 Verifica si el ID realmente se almacena
                        suggestionsBox.innerHTML = ""; // 📌 Oculta la lista después de la selección
                    } else {
                        console.error(`Error: No se encontró el ID para ${dog.name}`); // 📌 Detecta si el ID falta
                    }
                };
                

                suggestionsBox.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error buscando sugerencias:", error));
}

import { getDogData } from "./formHandler.js";
import { sendDogData } from "./apiRequests.js";
import { fetchDogSuggestions } from "./suggestions.js";

// 🔹 Capturar evento del formulario
document.getElementById("dogForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const dogData = getDogData();
    if (dogData) sendDogData(dogData);
});

// 🔹 Activar búsqueda predictiva para padres y madres
document.getElementById("father").addEventListener("input", (e) => fetchDogSuggestions(e.target.value, "father"));
document.getElementById("mother").addEventListener("input", (e) => fetchDogSuggestions(e.target.value, "mother"));

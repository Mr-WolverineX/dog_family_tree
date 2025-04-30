export function getDogData() {
    const dogData = {
        name: document.getElementById("name").value.trim(),
        breed: document.getElementById("breed").value.trim(),
        dob: document.getElementById("dob").value,
        gender: document.getElementById("gender").value.trim(),
        photo: document.getElementById("photo").value.trim(),
        father: document.getElementById("father").getAttribute("data-id") || null, // 📌 Enviar ID del padre o `null`
        mother: document.getElementById("mother").getAttribute("data-id") || null, // 📌 Enviar ID de la madre o `null`
    };

    if (!dogData.name || !dogData.breed) {
        alert("El nombre y la raza son obligatorios.");
        return null; // 📌 Retorna `null` si los datos son inválidos
    }

    return dogData; // 📌 Retorna los datos validados
}

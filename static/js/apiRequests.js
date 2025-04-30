
export function sendDogData(dogData) {

    fetch("/dogs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dogData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        console.log("Respuesta del servidor:", data);
        document.getElementById("dogForm").reset();
    })
    .catch(error => console.error("Error enviando los datos:", error));
}


export function approveRequest(dogId, descendantId) {
    fetch(`/dogs/${dogId}/approve-descendant`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ descendant_id: descendantId })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Solicitud aprobada:", data);
        alert("La solicitud ha sido aprobada con éxito.");
    })
    .catch(error => console.error("Error al aprobar solicitud:", error));
}

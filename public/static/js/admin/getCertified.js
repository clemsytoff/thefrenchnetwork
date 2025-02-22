document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:5000/api/v1/admin/certified", { method: 'GET' })
    .then(response => response.json())
    .then(certifeds => {
        let tableBody = document.getElementById("certifiedTable");
        if (certifeds.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='11'>Aucun utilisateur trouvé</td></tr>";
            return;
        }

        certifeds.forEach(certified => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${certified.user}</td>
                <td>${certified.date}</td>
                <td>${certified.reason}</td>
                <td>${certified.date}</td>
                <td>
                    <button onclick="certifiedUser(${certified.id})">Certifié</button>
                    <button onclick="uncertifiedUser(${certified.id})">Dé-Certifié</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error("Erreur :", error));
});
    
function certifiedUser(userId) {
    if (!confirm("Es-tu sûr de vouloir certifié cette utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "PUT" }) // Lien pour ajouter un utilisateur certifié
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Utilisateur certifié !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}

function uncertifiedUser(userId) {
    if (!confirm("Es-tu sûr de vouloir dé-certifié cette utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "PUT" }) // Lien pour enlevé un utilisateur certifié
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Utilisateur dé-certifié !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}
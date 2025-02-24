document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:5000/api/v1/admin/reports", { method: 'GET' })
    .then(response => response.json())
    .then(repports => {
        let tableBody = document.getElementById("repportTable");
        if (repports.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='11'>Aucun repport trouvé</td></tr>";
            return;
        }

        repports.forEach(repport => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${repport.id}</td>
                <td>${repport.reporter}</td>
                <td>${repport.reported_user}</td>
                <td>${repport.reported_post}</td>
                <td>${repport.reported_comment}</td>
                <td>${repport.reason}</td>
                <td>${repport.date}</td>
                <td>${repport.status}</td>
                <td>
                    <button onclick="confirmRepportUser(${repport.id})">Confimé</button>
                    <button onclick="unRepportUser(${repport.id})">Contredire</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error("Erreur :", error));
});

// certification de repport
function confirmRepportUser(userId) {
    if (!confirm("Es-tu sûr de vouloir repporter cette utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "" }) // Lien pour repport un utilisateur
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Utilisateur repport !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}

function unRepportUser(userId) {
    if (!confirm("Es-tu sûr de vouloir dé-repport cette utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "" }) // Lien pour dé-repport un utilisateur
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Utilisateur dé-repport !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}
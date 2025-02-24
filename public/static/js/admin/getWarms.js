document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:5000/api/v1/admin/warns", { method: 'GET' })
    .then(response => response.json())
    .then(warms => {
        let tableBody = document.getElementById("warmsTable");
        if (warms.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='11'>Aucun Bans trouvé</td></tr>";
            return;
        }

        warms.forEach(warms => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${warms.id}</td>
                <td>${warms.user}</td>
                <td>${warms.moderator}</td>
                <td>${warms.reason}</td>
                <td>${warms.date}</td>
                <td>
                    <button onclick="confirmBansUser(${warms.id})">Confimé</button>
                    <button onclick="unBansUser(${warms.id})">Contredire</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error("Erreur :", error));
});

// certification de warm
function confirmBansUser(userId) {
    if (!confirm("Es-tu sûr de vouloir d'avertissement de cette utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "" }) // Lien pour avertire un utilisateur
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Utilisateur avertis !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}

function unBansUser(userId) {
    if (!confirm("Es-tu sûr de vouloir d'enlever l'avertissement de cette utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "" }) // Lien pour dé-avertire un utilisateur
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Utilisateur dé-avertis !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}
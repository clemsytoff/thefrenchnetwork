document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:5000/api/v1/admin/bans", { method: 'GET' })
    .then(response => response.json())
    .then(bans => {
        let tableBody = document.getElementById("bansTable");
        if (bans.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='11'>Aucun Bans trouvé</td></tr>";
            return;
        }

        bans.forEach(ban => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${ban.id}</td>
                <td>${ban.user}</td>
                <td>${ban.moderator}</td>
                <td>${ban.reason}</td>
                <td>${ban.date}</td>
                <td>
                    <button onclick="confirmBansUser(${ban.id})">Confimé</button>
                    <button onclick="unBansUser(${ban.id})">Contredire</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error("Erreur :", error));
});

// certification de ban
function confirmBansUser(userId) {
    if (!confirm("Es-tu sûr de vouloir bannir cette utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "" }) // Lien pour bannir un utilisateur
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Utilisateur banni !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}

function unBansUser(userId) {
    if (!confirm("Es-tu sûr de vouloir dé-bannir cette utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "" }) // Lien pour dé-bannir un utilisateur
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Utilisateur dé-banni !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}
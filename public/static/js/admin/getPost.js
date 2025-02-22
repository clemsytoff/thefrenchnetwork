document.addEventListener("DOMContentLoaded", function () {
fetch("http://127.0.0.1:5000/api/v1/admin/posts", { method: 'GET' })
    .then(response => response.json())
    .then(posts => {
        let tableBody = document.getElementById("postTable");
        if (posts.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='11'>Aucun poste trouvé</td></tr>";
            return;
        }

        posts.forEach(post => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${post.id}</td>
                <td>${post.user}</td>
                <td>${post.content}</td>
                <td>${post.date}</td>
                <td>
                    <button onclick="repportPost(${user.id})">Repport</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error("Erreur :", error));
});

function repportPost(userId) {
    if (!confirm("Es-tu sûr de vouloir repport cet utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "PUT" }) // Lien pour ajouter un repport
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
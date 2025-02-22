document.addEventListener("DOMContentLoaded", function () {
fetch("http://127.0.0.1:5000/api/v1/admin/comments", { method: 'GET' })
    .then(response => response.json())
    .then(comments => {
        let tableBody = document.getElementById("commentTable");
        if (comments.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='11'>Aucun utilisateur trouvé</td></tr>";
            return;
        }

        comments.forEach(comment => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${comment.id}</td>
                <td>${comment.post}</td>
                <td>${comment.user}</td>
                <td>${comment.content}</td>
                <td>${comment.date}</td>
                <td>
                    <button onclick="repportComment(${comment.id})">Repport</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error("Erreur :", error));
});

function repportComment(userId) {
    if (!confirm("Es-tu sûr de vouloir repport ce commentaire ?")) return;

    fetch(`http://127.0.0.1:5000/...`, { method: "PUT" }) // Lien pour ajouter un repport de commentaire
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Commentaire repport !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}
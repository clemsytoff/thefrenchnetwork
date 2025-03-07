document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:5000/api/v1/admin/users", { method: 'GET' })
    .then(response => response.json())
    .then(users => {
        let tableBody = document.getElementById("userTable");
        if (users.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='11'>Aucun utilisateur trouvé</td></tr>";
            return;
        }

        users.forEach(user => {
            let birthDate = formatDateForInput(user.birth);

            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${user.id}</td>
                <td><input id="pseudo-${user.id}" value="${user.pseudo}"></td>
                <td><input id="name-${user.id}" value="${user.name}"></td>
                <td><input id="surname-${user.id}" value="${user.surname}"></td>
                <td><input id="email-${user.id}" value="${user.email}"></td>
                <td>
                    <input id="birth-${user.id}" value="${birthDate}" type="date">
                </td>
                <td><input id="password-${user.id}" type="password" placeholder="Laisser vide pour ne pas changer"></td>
                <td>${user.account_creation}</td>
                <td>
                    <select id="grade-${user.id}">
                        <option value="0" ${user.grade == 0 ? 'selected' : ''}>0 (Utilisateur)</option>
                        <option value="1" ${user.grade == 1 ? 'selected' : ''}>1 (Modérateur)</option>
                        <option value="2" ${user.grade == 2 ? 'selected' : ''}>2 (Responsable)</option>
                        <option value="3" ${user.grade == 3 ? 'selected' : ''}>3 (Admin)</option>
                    </select>
                </td>
                <td>
                    <select id="account_status-${user.id}">
                        <option value="actived" ${user.account_status == "actived" ? 'selected' : ''}>Actif</option>
                        <option value="discactived" ${user.account_status == "discactived" ? 'selected' : ''}>Désactivé</option>
                        <option value="suspended" ${user.account_status == "suspended" ? 'selected' : ''}>Suspendu</option>
                    </select>
                </td>
                <td>
                    <button onclick="editUser(${user.id})">Modifier</button>
                    <button onclick="deleteUser(${user.id})">Supprimer</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error("Erreur :", error));
});

function formatDateForInput(dateString) {
    let date = new Date(dateString);
    if (isNaN(date)) return "";

    let year = date.getFullYear();
    let month = String(date.getMonth() + 1).padStart(2, "0");
    let day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
}

function editUser(userId) {
    let pseudo = document.getElementById(`pseudo-${userId}`).value;
    let name = document.getElementById(`name-${userId}`).value;
    let surname = document.getElementById(`surname-${userId}`).value;
    let email = document.getElementById(`email-${userId}`).value;
    let birthInput = document.getElementById(`birth-${userId}`).value;
    let password = document.getElementById(`password-${userId}`).value;
    let grade = document.getElementById(`grade-${userId}`).value;
    let account_status = document.getElementById(`account_status-${userId}`).value;

    // Conversion de la date (YYYY-MM-DD → YYYY/MM/DD)
    const birthParts = birthInput.split('-');
    const birth = `${birthParts[0]}/${birthParts[1]}/${birthParts[2]}`;

    let userData = { pseudo, name, surname, email, birth, grade, account_status };
    if (password) userData.password = password;

    fetch(`http://127.0.0.1:5000/api/v1/admin/user/edit/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Erreur : " + data.error);
        } else {
            alert("Utilisateur mis à jour !");
            location.reload();
        }
    })
    .catch(error => console.error("Erreur :", error));
}

function deleteUser(userId) {
    if (!confirm("Es-tu sûr de vouloir supprimer cet utilisateur ?")) return;

    fetch(`http://127.0.0.1:5000/api/v1/admin/user/delete/${userId}`, { method: "DELETE" })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Erreur : " + data.error);
            } else {
                alert("Utilisateur mis à jour !");
                location.reload();
            }
        })
        .catch(error => console.error("Erreur :", error));
}
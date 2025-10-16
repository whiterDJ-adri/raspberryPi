

document.addEventListener("DOMContentLoaded", () => {
    loadUsers();

    // Logout
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", async () => {
            const response = await fetch("/logout");
            const data = await response.json();
            alert(data.message);
            window.location.href = data.redirect;
        });
    }
});

async function loadUsers() {
    try {
        const response = await fetch("/login/users", { credentials: "include" });
        console.log("Status:", response.status);
        const text = await response.text();
        console.log("Response text:", text);

        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }

        const users = JSON.parse(text);
        const tableBody = document.getElementById("userTable");
        tableBody.innerHTML = "";

        users.forEach(user => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.isAdmin ? "✔️" : "❌"}</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="deleteUser('${user.email}')">
                        Eliminar
                    </button>
                </td>
            `;
            tableBody.appendChild(tr);
        });

    } catch (error) {
        console.error("Error en loadUsers:", error);
        alert("No se pudieron cargar los usuarios.");
    }
}


async function deleteUser(email) {
    if (!confirm(`¿Seguro que quieres eliminar a ${email}?`)) return;

    try {
        const response = await fetch("/login/delete", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();
        alert(data.message);
        loadUsers(); // Recarga la tabla
    } catch (error) {
        console.error("Error al eliminar usuario:", error);
        alert("Error al eliminar el usuario.");
    }
}

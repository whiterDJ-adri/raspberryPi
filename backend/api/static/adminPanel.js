document.addEventListener("DOMContentLoaded", () => {
    loadUsers();

    // Logout
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", async () => {
            try {
                const response = await fetch("/logout");
                const data = await response.json();
                alert(data.message);
                window.location.href = data.redirect;
            } catch (error) {
                console.error("Error al cerrar sesión:", error);
                alert("No se pudo cerrar sesión.");
            }
        });
    }

    // Crear usuario - botón del modal
    const saveUserBtn = document.getElementById("saveUserBtn");
    if (saveUserBtn) {
        saveUserBtn.addEventListener("click", createUser);
    }
});


// Cargar lista de usuarios
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
                <td>${user.isAdmin ? "  Si" : "No"}</td>
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


// 🟡 Crear nuevo usuario (desde el modal)
async function createUser() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const isAdmin = document.getElementById("isAdmin").checked;

    if (!name || !email || !password) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    try {
        const response = await fetch("/login/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ name, email, password, isAdmin }),
        });

        const data = await response.json();
        alert(data.message);

        if (response.ok) {
            // Cierra el modal y limpia el formulario
            const modal = bootstrap.Modal.getInstance(document.getElementById("createUserModal"));
            if (modal) modal.hide();

            document.getElementById("createUserForm").reset();
            loadUsers(); // Recarga la tabla
        }
    } catch (error) {
        console.error("Error al crear usuario:", error);
        alert("Error al crear el usuario.");
    }
}


// 🔴 Eliminar usuario
async function deleteUser(email) {
    if (!confirm(`¿Seguro que quieres eliminar a ${email}?`)) return;

    try {
        const response = await fetch("/login/delete", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({ email })
        });

        const data = await response.json();
        alert(data.message);

        if (response.ok) {
            loadUsers(); // Recarga la tabla
        }
    } catch (error) {
        console.error("Error al eliminar usuario:", error);
        alert("Error al eliminar el usuario.");
    }
}

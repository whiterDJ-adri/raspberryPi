document.addEventListener("DOMContentLoaded", () => {
    const userTable = document.getElementById("userTable");

    // Cargar usuarios al iniciar
    fetch("/users")
        .then(response => response.json())
        .then(users => {
            userTable.innerHTML = "";
            users.forEach(user => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${user.name || "Sin nombre"}</td>
                    <td>${user.email}</td>
                    <td>${user.isAdmin ? "Sí" : "No"}</td>
                    <td>
                        <button class="btn btn-danger btn-sm delete-btn" data-email="${user.email}">
                            Eliminar
                        </button>
                    </td>
                `;
                userTable.appendChild(row);
            });

            // Asignar eventos de eliminar
            document.querySelectorAll(".delete-btn").forEach(btn => {
                btn.addEventListener("click", e => {
                    const email = e.target.dataset.email;
                    if (confirm(`¿Eliminar al usuario ${email}?`)) {
                        fetch("/delete", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({ email }),
                        })
                            .then(res => res.json())
                            .then(data => {
                                alert(data.message);
                                location.reload(); // refrescar tabla
                            });
                    }
                });
            });
        })
        .catch(err => console.error("Error cargando usuarios:", err));
});

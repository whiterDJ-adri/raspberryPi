const form = document.querySelector(".loginForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://localhost:5000/login/login", {
			method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    console.log("Respuesta del servidor:", data);
    window.location.href = data.redirect;
  } catch (error) {
    console.error("Error en el fetch:", error);
  }
});

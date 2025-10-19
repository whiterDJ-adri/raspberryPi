document.addEventListener("DOMContentLoaded", () => {
	// Configurar botón de logout
	const logoutBtn = document.getElementById("logoutBtn");
	if (logoutBtn) {
		logoutBtn.addEventListener("click", async () => {
			try {
				const response = await fetch("/login/logout");
				const data = await response.json();
				alert(data.message);
				window.location.href = data.redirect;
			} catch (error) {
				console.error("Error al cerrar sesión:", error);
				alert("No se pudo cerrar sesión.");
			}
		});
	}

	// Inicializar estado del botón de streaming
	const streamBtn =
		document.getElementById("streaming") ||
		document.getElementById("streamingBtn") ||
		document.getElementById("straming");
	if (streamBtn && !streamingActive) {
		streamBtn.innerHTML =
			'<i class="bi bi-play-circle me-2"></i>Iniciar Transmisión';
	}
});

async function pedir_fotos() {
	let gallery = document.getElementById("gallery");
	gallery.innerHTML = "";

	const api = "http://localhost:5000/api/photo";

	try {
		// Pedimos todas las fotos a la api a traves del fetch (GET)
		const response = await fetch(api);
		// Transformamos el objeto que nos devuelve a json
		const data = await response.json();
		let rutas = [];
		data.forEach((img) => {
			let ruta = `/api/photo/screenshots/${img.filename}`;
			console.log("Ruta: ", ruta);
			rutas.push(ruta);
		});

		rutas.forEach((r) => {
			gallery.innerHTML += `<img src="${r}" class="w-25" />`;
		});

		// Para cambiar el contrador de las fotos
		contador = document.getElementById("photoCount");
		contador.innerHTML = `${rutas.length} fotos`;
	} catch (err) {
		console.error("Error: ", err);
	}
}

let streamingActive = false;

function streaming() {
	const videoFeed = document.getElementById("videoFeed");
	const placeholder = document.getElementById("videoPlaceholder");
	const streamBtn =
		document.getElementById("streaming") ||
		document.getElementById("streamingBtn") ||
		document.getElementById("straming");

	// Verificar que los elementos existen
	if (!videoFeed || !placeholder || !streamBtn) {
		console.error(
			"No se encontraron los elementos necesarios para el streaming"
		);
		alert("Error: No se encontraron los elementos de video en la página");
		return;
	}

	if (!streamingActive) {
		// Iniciar streaming
		console.log("Iniciando streaming...");

		// Cambiar botón antes de cargar el video
		streamBtn.innerHTML =
			'<i class="bi bi-hourglass-split me-2"></i>Conectando...';
		streamBtn.disabled = true;

		// Configurar eventos del video
		videoFeed.onload = () => {
			console.log("Stream conectado correctamente");
			streamBtn.innerHTML =
				'<i class="bi bi-pause-circle me-2"></i>Pausar Transmisión';
			streamBtn.disabled = false;
		};

		videoFeed.onerror = () => {
			console.error("Error al cargar el stream");
			streamBtn.innerHTML =
				'<i class="bi bi-play-circle me-2"></i>Iniciar Transmisión';
			streamBtn.disabled = false;
			alert("Error: No se pudo conectar al video en vivo");
			streamingActive = false;
			return;
		};

		// Iniciar stream
		videoFeed.src = "/api/photo/video?" + new Date().getTime(); // Cache busting
		videoFeed.style.display = "block";
		placeholder.classList.add("d-none");
		streamingActive = true;

		// Timeout para evitar que se quede cargando indefinidamente
		setTimeout(() => {
			if (streamBtn.innerHTML.includes("Conectando")) {
				streamBtn.innerHTML =
					'<i class="bi bi-pause-circle me-2"></i>Pausar Transmisión';
				streamBtn.disabled = false;
			}
		}, 3000);
	} else {
		// Pausar streaming
		console.log("Pausando streaming...");
		streamBtn.innerHTML =
			'<i class="bi bi-play-circle me-2"></i>Iniciar Transmisión';
		streamBtn.disabled = false;
		videoFeed.style.display = "none";
		placeholder.classList.remove("d-none");
		videoFeed.src = ""; // Detener la carga del video
		videoFeed.onload = null; // Limpiar eventos
		videoFeed.onerror = null;
		streamingActive = false;
	}
}

async function filterDate() {
	const dateInput = document.getElementById("dateFilter").value;

	if (!dateInput) {
		alert("Por favor, selecciona una fecha");
		return;
	}

	let gallery = document.getElementById("gallery");
	gallery.innerHTML = "";

	// En la url se añade un campo opcional date
	const api = `http://localhost:5000/api/photo?date=${dateInput}`;

	try {
		const response = await fetch(api);
		const data = await response.json();

		let rutas = [];
		data.forEach((img) => {
			let ruta = `/api/photo/screenshots/${img.filename}`;
			console.log("Ruta: ", ruta);
			rutas.push(ruta);
		});

		rutas.forEach((r) => {
			gallery.innerHTML += `<img src="${r}" class="w-25" />`;
		});

		// Actualizar el contador de fotos
		let contador = document.getElementById("photoCount");
		const photoText = rutas.length === 1 ? "foto" : "fotos";
		contador.innerHTML = `${rutas.length} ${photoText}`;

		if (rutas.length === 0) {
			gallery.innerHTML =
				'<p class="text-muted">No se encontraron fotos para esta fecha</p>';
		}
	} catch (err) {
		console.error("Error: ", err);
		alert("Error al filtrar las fotos");
	}
}

async function deleteAllPhotos() {
	if (!confirm("¿Seguro que quieres eliminar todas las fotos?")) return;

	try {
		await fetch("/api/photo/photos/removeAll", { method: "DELETE" });
		pedir_fotos();
	} catch (err) {
		console.error("Error: ", err);
	}
}

async function eliminarFotoPorFecha() {
	const dateInput = document.getElementById("dateFilter").value;
	if (!dateInput) {
		alert("Por favor, selecciona una fecha");
		return;
	}
	if (
		!confirm(`¿Seguro que quieres eliminar todas las fotos del ${dateInput}?`)
	)
		return;

	try {
		const encodedDate = encodeURIComponent(dateInput);
		const res = await fetch(`/api/photo/photos/removeByDate/${encodedDate}`, {
			method: "DELETE",
		});

		if (!res.ok) {
			// intentar leer mensaje de error si viene en json/text
			let mensajeError = "";
			try {
				const t = await res.text();
				mensajeError = t || res.statusText;
			} catch {
				mensajeError = res.statusText;
			}
			alert(`No se pudieron eliminar las fotos: ${mensajeError}`);
			return;
		}

		// leer posible mensaje de respuesta
		let result = null;
		try {
			result = await res.json();
		} catch (error) {
			console.error("Error al parsear JSON de respuesta:", error);
		}

		alert(
			result && result.message
				? result.message
				: `Fotos del ${dateInput} eliminadas`
		);
		await pedir_fotos();
	} catch (err) {
		console.error("Error: ", err);
	}
}

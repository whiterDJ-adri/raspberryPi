document.addEventListener("DOMContentLoaded", () => {
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
	const text = document.getElementById('textVideo');

	videoFeed.src = "/api/photo/video";
    videoFeed.style.display = 'block'; 
	placeholder.classList.add("d-none");
	
	const streamBtn = document.getElementById("straming") || document.getElementById("streamingBtn");

	if(!streamingActive){
		streamBtn.innerHTML = '<i class="bi bi-pause-circle me-2"></i>Pausar Transmisión';
		videoFeed.src = "/api/photo/video"; 
		videoFeed.style.display = 'block'; 
		placeholder.classList.add("d-none");
		streamingActive = true;
	}else{
		streamBtn.innerHTML = '<i class="bi bi-play-circle me-2"></i>Iniciar Transmisión';
		videoFeed.style.display = 'none';
		placeholder.classList.remove("d-none");
		videoFeed.src = ""; // Detener la carga del video
		streamingActive = false;
	}

>>>>>>> bcd1539e1009e9e99339cde6b097150fa0c5dc22
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

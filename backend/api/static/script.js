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

function streaming(){
    document.getElementById('videoFeed').src = '/api/photo/video';
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

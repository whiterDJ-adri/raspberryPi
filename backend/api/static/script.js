document.addEventListener("DOMContentLoaded", () => {
    const adminBtn = document.getElementById("adminBtn");
    if (adminBtn) {
        adminBtn.addEventListener("click", () => {
            window.location.href = "/dashboard/admin/boton";
        });
    }
});

async function pedir_fotos() {
    let gallery = document.getElementById("gallery");
    gallery.innerHTML = "";

    const api = 'http://localhost:5000/api/photo';
    
    try {
        // Pedimos todas las fotos a la api a traves del fetch (GET)
        const response = await fetch(api);
        // Transformamos el objeto que nos devuelve a json
        const data = await response.json();
        let rutas = [];
        data.forEach(img => {
            let ruta = `/api/photo/screenshots/${img.filename}`;
            console.log("Ruta: ", ruta);
            rutas.push(ruta);
        });

        rutas.forEach(r => {
            gallery.innerHTML += `<img src="${r}" class="w-25" />`;
        });

        // Para cambiar el contrador de las fotos
        contador = document.getElementById("photoCount");
        contador.innerHTML = `${rutas.length} fotos`;
    } catch(err) {
        console.error("Error: ", err);
    }
}

async function streaming(){
    document.getElementById('videoFeed').src = '/api/photo/video';
}
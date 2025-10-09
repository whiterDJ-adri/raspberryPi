async function pedir_fotos() {
    let gallery = document.getElementById("gallery");
    gallery.innerHTML = "";

    const api = 'http://localhost:5000/api/photo';
    
    try {
        // Pedimos todas las fotos a la api a traves del fetch (GET)
        const response = await fetch(api);
        // Transformamos el objeto que nos devuelve a json
        const data = await response.json();
        console.log("Data: ", data);
        let rutas = [];
        
        data[0].forEach(img => {
            let ruta = `/api/photo/screenshots/${img.filename}`;
            rutas.push(ruta);
        });

        rutas.forEach(r => {
            gallery.innerHTML += `<img src="${r}" class="w-25" />`;
        });
    } catch(err) {
        console.error("Error: ", err);
    }
}
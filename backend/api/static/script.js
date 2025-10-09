async function pedir_fotos() {
    let gallery = document.getElementById("gallery");
    const api = '/api/photo';
    try {
        // Pedimos todas las fotos a la api a traves del fetch (GET)
        const response = await fetch(api);
        // Transformamos el objeto que nos devuelve a json
        const data = await response.json();
        console.log("Data: ", data);
        let rutas = [];
        for(let reg of data[0]){
            let ruta = `media/screenshots/${reg.filename}`;
            rutas.push(ruta);
        }

        console.log("Rutas: ", rutas);
        console.log(data);

        rutas.forEach(r => {
            gallery.innerHTML += `<img src="${r}">`;
        });
    } catch(err) {
        console.error("Error: ", err);
    }
}
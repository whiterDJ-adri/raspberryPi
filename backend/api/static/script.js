async function pedir_fotos() {
    let gallery = document.getElementById("galery");
    const api = '/api/photo';
    try {
        // Pedimos todas las fotos a la api a traves del fetch (GET)
        const response = await fetch(api);
        // Transformamos el objeto que nos devuelve a json
        const data = await response.json();

        console.log(data);
    } catch(err) {
        console.error("Error: ", err);
    }
}
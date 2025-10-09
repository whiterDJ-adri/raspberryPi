async function pedir_fotos() {
    let gallery = document.getElementById("galery");
    const api = '/api/photo';
    try {
        const response = await fetch(api);
        const data = await response.json();

        console.log(data);
    } catch(err) {
        console.error("Error: ", err);
    }
}
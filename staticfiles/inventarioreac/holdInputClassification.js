// Función para configurar los selectores según los valores en la URL o valores por defecto
function configurarSelectoresDesdeURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const nameValue = urlParams.get('name');
    
    const idValue = urlParams.get('id_classification');
    

    const nameInput = document.getElementById('name');
   
    const idInput = document.getElementById('id_classification');


    if (nameValue !== null) {
        nameInput.value = nameValue;
    } else {
        nameInput.value = ''; // Valor por defecto de la entrada "name"
    }

    
    if (idValue !== null) {
        idInput.value = idValue;
    } else {
        idInput.value = ''; // Valor por defecto de la entrada "id_classification"
    }
}

// Esperar 200 ms después de la carga para configurar los selectores desde la URL
window.addEventListener('load', function () {
    setTimeout(configurarSelectoresDesdeURL, 50);
});

// Función para configurar los selectores según los valores en la URL o valores por defecto
function configurarSelectoresDesdeURL() {
    const urlParams = new URLSearchParams(window.location.search);
    
    const idLabValue = urlParams.get('id_laboratorio');
    const nameValue = urlParams.get('name');    
  
    const startDateValue = urlParams.get('start_date');
    const endDateValue = urlParams.get('end_date');

    const idLabInput = document.getElementById('id_laboratorio');
    const nameInput = document.getElementById('name');   
  
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');


    if (idLabValue !== null) {
        idLabInput.value = idLabValue;
    } else {
        idLabInput.value = lab_id; // Valor por defecto de la entrada "id_lab"
    }

    if (nameValue !== null) {
        nameInput.value = nameValue;
    } else {
        nameInput.value = ''; // Valor por defecto de la entrada "name"
    }

    


    if (startDateValue !== null) {
        startDateInput.value = startDateValue;
    } else {
        startDateInput.value = ''; // Valor por defecto de la entrada "start_date"
    }

    if (endDateValue !== null) {
        endDateInput.value = endDateValue;
    } else {
        endDateInput.value = ''; // Valor por defecto de la entrada "end_date"
    }
}

// Esperar 200 ms después de la carga para configurar los selectores desde la URL
window.addEventListener('load', function () {
    setTimeout(configurarSelectoresDesdeURL, 50);
});

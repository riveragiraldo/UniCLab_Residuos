// Evento click para mostrar SweetAlert con la información del usuario
document.querySelectorAll('.detail-register').forEach(element => {
    element.addEventListener('click', function () {
        const registroNombre = this.getAttribute('data-register-name');
        const registroDescripcion = this.getAttribute('data-register-description');        
        
        const registro = obtenerInformacionRegistro(registroNombre,registroDescripcion);
        mostrarSweetAlert(registro);
    });
});

// Función para obtener la información del usuario basado en su ID (puedes hacer la solicitud al servidor)
function obtenerInformacionRegistro(nombre,descripcion) {

    const registro = {
        nombre: nombre,
        descripcion:descripcion,
        
        

    };
    return registro;
}

// Función para mostrar la SweetAlert con la información del usuario
function mostrarSweetAlert(registro) {
    Swal.fire({
        icon: 'info',
        title: `Detalle de clasificación de residuos`,
        html: `
            <div class="card" style="text-align: left;">
                <br>
                <div class="card-body">
                    <h5>Información principal:</h5>
                    <ul class="list-unstyled">
                        
                        <li><strong>Nombre:</strong> ${registro.nombre}</li>
                        <li><strong>Descripción:</strong> ${registro.descripcion}</li>
                    </ul>
                    <br>
                    <h5>Información adicional:</h5>
                    <ul class="list-unstyled">
                        <li><strong>Más información:</strong> Visite <a target='_blank' href="https://www.minambiente.gov.co/wp-content/uploads/2021/06/Decreto-1076-de-2015.pdf">Decreto número 1076 de 2015</a> MINISTERIO DE AMBIENTE Y DESARROLLO SOSTENIBLE</li>
                        
                        
                    </ul>
                </div>
            </div>
        `,
        showConfirmButton: true,
        confirmButtonText: 'Aceptar',
        customClass: 'custom-swal-class' // Clase CSS personalizada para dar estilo a la alerta
    });
}

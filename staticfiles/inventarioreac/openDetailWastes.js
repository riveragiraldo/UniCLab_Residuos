// Evento click para mostrar SweetAlert con la información del usuario
document.querySelectorAll('.detalle-residuo').forEach(element => {
    element.addEventListener('click', function () {
        const registroId = this.getAttribute('registro-id');
        const registroFechaCreacion = this.getAttribute('registro-fecha-creacion');        
        const registroDependencia = this.getAttribute('registro-dependencia');
        const registroNombre = this.getAttribute('registro-nombre');
        const registroCantidad = this.getAttribute('registro-cantidad');
        const registroEnvase = this.getAttribute('registro-envases');
        const registroTotal = this.getAttribute('registro-total');
        const registroClasificacion = this.getAttribute('registro-clasificacion');
        const registroEstado = this.getAttribute('registro-estado');
        const registroFechaRegistro = this.getAttribute('registro-fecha-registro');
        const registroCreador = this.getAttribute('registro-creador');
        const registroCreadorEmail = this.getAttribute('registro-creador-email');
        const registroFechaActualizacion = this.getAttribute('registro-fecha-actualizacion');
        const registroActualizador = this.getAttribute('registro-actualizador');

        const registro = obtenerInformacionRegistro(registroId, registroFechaCreacion, registroDependencia, registroNombre, registroCantidad, registroEnvase, registroTotal, registroClasificacion, registroEstado, registroFechaRegistro, registroCreador, registroCreadorEmail, registroFechaActualizacion, registroActualizador);
        mostrarSweetAlert(registro);
    });
});

// Función para obtener la información del usuario basado en su ID (puedes hacer la solicitud al servidor)
function obtenerInformacionRegistro(id, fechacreacion, dependencia, nombre, cantidad, envase, total, clasificacion, estado, fecharegistro, creador, emailcreador, fechaactualizacion, actualizador) {

    const registro = {
        id: id,
        fechacreacion:fechacreacion,
        dependencia:dependencia,
        nombre:nombre,
        cantidad:cantidad,
        envase:envase,
        total:total,
        clasificacion:clasificacion,
        estado:estado,
        fecharegistro:fecharegistro,
        creador:creador,
        emailcreador:emailcreador,
        fechaactualizacion:fechaactualizacion,
        actualizador:actualizador,
    };
    return registro;
}

// Función para mostrar la SweetAlert con la información del usuario
function mostrarSweetAlert(registro) {
    Swal.fire({
        icon: 'info',
        title: `Detalle del registro de residuos`,
        html: `
            <div class="card" style="text-align: left;">
                <br>
                <div class="card-body">
                    <h5>Información principal:</h5>
                    <ul class="list-unstyled">
                        
                        <li><strong>Fecha de Registro:</strong> ${registro.fechacreacion}</li>
                        <li><strong>Id del Registro:</strong> ${registro.id}</li>
                        <li><strong>Dependencia:</strong> ${registro.dependencia}</li>
                        <li><strong>Nombre del Residuo:</strong> ${registro.nombre}</li>
                        <li><strong>Cantidad:</strong> ${registro.cantidad}</li>
                        <li><strong>Cantidad Envases:</strong> ${registro.envase}</li>
                        <li><strong>Total Residuo:</strong> ${registro.total}</li>
                        <li><strong>Clasificación Y - A:</strong> ${registro.clasificacion}</li>
                        <li><strong>Estado:</strong> ${registro.estado}</li>
                    </ul>
                    <br>
                    <h5>Información adicional:</h5>
                    <ul class="list-unstyled">
                        <li><strong>Fecha de Creación:</strong> ${registro.fecharegistro}</li>
                        <li><strong>Responsable del Registro:</strong> ${registro.creador}</li>
                        <li><strong>Correo Electrónico:</strong> ${registro.emailcreador}</li>
                        <li><strong>Última Actualización:</strong> ${registro.fechaactualizacion}</li>
                        <li><strong>Actualizado por:</strong> ${registro.actualizador}</li>
                    </ul>
                </div>
            </div>
        `,
        showConfirmButton: true,
        confirmButtonText: 'Aceptar',
        customClass: 'custom-swal-class' // Clase CSS personalizada para dar estilo a la alerta
    });
}

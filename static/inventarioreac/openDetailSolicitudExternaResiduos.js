// Evento click para mostrar SweetAlert con la información del solicitud
document.querySelectorAll('.solicitud-externa').forEach(element => {
    element.addEventListener('click', function () {
        const solicitudId = this.getAttribute('data-sol-id');
        const solicitudDate = this.getAttribute('data-solicitud-date');
        const solicitudTipoLab = this.getAttribute('data-solicitud-lab');
        const solicitudTipoSolicitud = this.getAttribute('data-solicitud-tipo');
        const solicitudMensaje = this.getAttribute('data-solicitud-mensaje');
        const solicitudAdjuntos = this.getAttribute('data-solicitud-adjuntos');
        const solicitudAdjuntosUrl = this.getAttribute('data-solicitud-adjuntos-url');
        const solicitudName = this.getAttribute('data-solicitud-nombre');
        const solicitudDepartment = this.getAttribute('data-solicitud-area');
        const solicitudPhoneNumber = this.getAttribute('data-solicitud-telefono');
        const solicitudEmail = this.getAttribute('data-solicitud-email');
        const solicitudEncondedId = this.getAttribute('data-solicitud-encoded-id');
        const solicitudHasAnswered = this.getAttribute('data-solicitud-respondido');

        const solicitud = obtenerInformacionSolicitud(solicitudId, solicitudTipoSolicitud, solicitudDate, solicitudTipoLab, solicitudMensaje, solicitudAdjuntos, solicitudAdjuntosUrl, solicitudName, solicitudDepartment, solicitudPhoneNumber, solicitudEmail, solicitudEncondedId, solicitudHasAnswered);
        mostrarSweetAlert(solicitud);
    });
});

// Función para obtener la información del solicitud basado en su ID (puedes hacer la solicitud al servidor)
function obtenerInformacionSolicitud(solicitud_id, tipo_solicitud, date, lab, mensaje, adjuntos, adjuntos_url, nombres, area, telefono, email, id_codificado, respondido) {
    const solicitud = {
        solicitud_id: solicitud_id,
        tipo_solicitud: tipo_solicitud,
        date: date,
        lab: lab,
        mensaje: mensaje,
        adjuntos: adjuntos,
        adjuntos_url: adjuntos_url,
        nombres: nombres,
        area: area,
        telefono: telefono,
        email: email,
        id_codificado: id_codificado,
        respondido: respondido,
    };
    return solicitud;
}

// Función para mostrar la SweetAlert con la información del solicitud
function mostrarSweetAlert(solicitud) {
    const adjuntos = solicitud.adjuntos;
    console.log(adjuntos);

    let archivos_adjuntos = '';
    if (adjuntos) {
        archivos_adjuntos = `<a href='${solicitud.adjuntos_url}' target='_blank'>${adjuntos}</a>`;
    } else {
        archivos_adjuntos = '';
    }

    let footerHtml = '';
    let showCancelButton = true;
    let confirmButtonText = 'Sí';
    let cancelButtonText = 'No';
    let preConfirm = () => new Promise((resolve) => resolve());

    if (solicitud.respondido === 'Pendiente por responder') {
        footerHtml = `
            <div class="card-footer" style='margin-top:10px'>
                <p>¿Desea enviar una notificación de lectura al remitente de la solicitud?</p>
            </div>
        `;
    } else {
        footerHtml = `
            <div class="card-footer text-center" style='margin-top:10px; background-color: #f8d7da; color: #721c24; height: 60px; display: flex; align-items: center; justify-content: center;'>
                <p>Ya has dado respuesta a esta solicitud.</p>
            </div>
        `;
        showCancelButton = false;
        confirmButtonText = 'Aceptar';
        cancelButtonText = '';
        preConfirm = () => {
            solicitudLeida(solicitud.id_codificado, '');
            return new Promise((resolve) => resolve());
        };
    }

    Swal.fire({
        icon: 'info',
        title: `Detalle de solicitud`,
        html: `
            <div class="card" style="text-align: left;">
                <div class="card-header">
                    Detalle de registro de solicitud número ${solicitud.solicitud_id} de ${solicitud.date}
                </div>
                <br>
                <div class="card-body">
                    <h5>Información principal:</h5>
                    <ul class="list-unstyled">
                        <li><strong>Consecutivo:</strong> ${solicitud.solicitud_id}</li>
                        <li><strong>Laboratorio al cual va dirigido:</strong> ${solicitud.lab}</li>
                        <li><strong>Fecha de registro:</strong> ${solicitud.date}</li>
                        <li><strong>Asunto:</strong> ${solicitud.tipo_solicitud}</li>
                        <li><strong>Mensaje:</strong> ${solicitud.mensaje}</li>
                        <li><strong>Archivos Adjuntos:</strong> ${archivos_adjuntos}</li>
                        <li><strong>Estado de respuesta:</strong> ${solicitud.respondido}</li>
                    </ul>
                    <br>
                    <h5>Datos del remitente</h5>
                    <ul class="list-unstyled">
                        <li><strong>Nombres y apellidos:</strong> ${solicitud.nombres}</li>
                        <li><strong>Área:</strong> ${solicitud.area}</li>
                        <li><strong>Teléfono:</strong> ${solicitud.telefono}</li>
                        <li><strong>Correo Electrónico:</strong> ${solicitud.email}</li>
                    </ul>
                </div>
                ${footerHtml}
            </div>
        `,
        showCancelButton: showCancelButton,
        confirmButtonText: confirmButtonText,
        cancelButtonText: cancelButtonText,
        preConfirm: preConfirm
    }).then((result) => {
        if (result.isConfirmed) {
            if (solicitud.respondido === 'Pendiente por responder') {
                Swal.fire({
                    title: 'Días de respuesta',
                    text: 'Escriba el número de días en que se dará respuesta al registro.',
                    input: 'number',
                    inputAttributes: {
                        autocapitalize: 'off',
                        min: 1,
                        step: 1,
                    },
                    showCancelButton: true,
                    confirmButtonText: 'Enviar',
                    cancelButtonText: 'Cancelar',
                    showLoaderOnConfirm: true,
                    preConfirm: (days) => {
                        if (!days || days < 1) {
                            Swal.showValidationMessage('Por favor ingrese un número entero mayor o igual a 1');
                            return false;
                        }

                        return fetch(`/UniCLab_Residuos/Solicitudes_Externas/Enviar_Notificacion/?dias=${days}&encoded_id=${solicitud.id_codificado}`, {
                            method: 'GET',
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                            },
                        })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error(response.statusText);
                                }
                                // Verificar el estado de la respuesta
                                return response.json().then(data => {
                                    if (data.status === 'success') {
                                        Swal.fire({
                                            icon: 'success',
                                            title: 'Notificación enviada',
                                            text: 'Notificación de lectura enviada con éxito.'
                                        }).then(() => {
                                            solicitudLeida(solicitud.id_codificado, '');
                                        });
                                    } else {
                                        throw new Error(data.message || 'Error al enviar la notificación de lectura.');
                                    }
                                });
                            })
                            .catch(error => {
                                Swal.showValidationMessage(`Request failed: ${error}`);
                            });
                    }
                });
            } else {
                solicitudLeida(solicitud.id_codificado, '');
                // Swal.fire({
                //     icon: 'success',
                //     title: 'Notificación enviada',
                //     text: 'Notificación de lectura enviada con éxito.'
                // });
            }
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            solicitudLeida(solicitud.id_codificado, '');
        }
    });
}

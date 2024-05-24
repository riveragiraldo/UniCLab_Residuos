function cerrarVentana() {
    Swal.fire({
        title: 'Notificación de lectura',
        text: '¿Desea enviar notificación de lectura al remitente?',
        icon: 'warning',
        showCancelButton: true,
        showDenyButton: true,
        confirmButtonText: 'Sí',
        denyButtonText: 'No',
        cancelButtonText: 'Cancelar',
        allowOutsideClick: false,
        allowEscapeKey: false,
    }).then((result) => {
        if (result.isConfirmed) {
            // Opción "Sí"
            Swal.fire({
                title: 'Días de respuesta',
                text: 'Escriba el número de días en que se dará respuesta al registro.',
                input: 'number',
                inputAttributes: {
                    autocapitalize: 'off',
                    min: 1,
                    step: 1,
                    required: true,
                    title: 'Debe diligenciar de manera obligatoria números enteros positivos'
                },
                showCancelButton: true,
                confirmButtonText: 'Enviar',
                cancelButtonText: 'Cancelar',
                showLoaderOnConfirm: true,
                preConfirm: (days) => {
                    return fetch(url+"?pdf_filename="+pdf_filename+"&solicitud="+solicitud+"&notification=True&days=" + days)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(response.statusText);
                            }
                            return response.json();
                        })
                        .catch(error => {
                            Swal.showValidationMessage(
                                `Request failed: ${error}`
                            );
                        });
                },
                allowOutsideClick: () => !Swal.isLoading()
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire('¡Respuesta enviada!', '', 'success');
                    window.close();
                }
            });
        } else if (result.isDenied) {
            // Opción "No"
            sendRequest('False');
        }
        // Si es cancelado, no se hace nada
    });
}

function sendRequest(notification) {
    fetch(url+"?pdf_filename="+pdf_filename+"&solicitud="+solicitud+"&notification=" + notification, {
        method: 'GET'
    }).then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.close();
            } else {
                Swal.fire('Error', 'Error al eliminar el archivo PDF.', 'error');
            }
        });
}

// Funcion para borrar solicitud cuando se cierra no envía correo
window.addEventListener('beforeunload', function () {
    // Enviar mensaje a la ventana padre para recargar después de 2 segundos
    if (window.opener && !window.opener.closed) {
        window.opener.postMessage('close_and_refresh', '*');
    }

    // Hacer una solicitud para eliminar el archivo PDF
    fetch(url+"?pdf_filename="+pdf_filename+"&solicitud="+solicitud+"&notification=False", {
        method: 'GET'
    });
});


$(document).ready(function () {
    $('#label_substances_form').submit(function (event) {
        // Evitar que el formulario se envíe de forma convencional
        event.preventDefault();

        // Mostrar el mensaje de carga con una barra de progreso
        Swal.fire({
            title: 'Por favor espere...',
            html: 'Agregando información',
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading();
                // Crear un objeto FormData para enviar archivos
                var formData = new FormData(this);

                // Realizar la solicitud AJAX
                $.ajax({
                    type: 'POST',
                    url: $(this).attr('action'),
                    data: formData,
                    // Necesitas configurar estas opciones para enviar archivos correctamente
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        // Ocultar el mensaje de carga
                        Swal.close();

                        // Manejar la respuesta del servidor
                        if (response.success) {
                            // Mostrar la notificación con SweetAlert2
                            Swal.fire({
                                icon: 'success',
                                title: 'Envío Exitoso',
                                text: response.message,
                                confirmButtonText: 'Aceptar'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    if (window.opener) { // Verifica si hay una ventana padre y si no está cerrada
                                        window.opener.location.reload(); // Actualiza la ventana padre
                                        setTimeout(() => {
                                            window.close(); // Cierra la ventana hija después de 100 ms
                                        }, 200);
                                    } else {
                                        window.location.reload(); // Actualiza la ventana actual si no hay ventana padre o está cerrada
                                    }
                                }
                            });

                            // Puedes realizar acciones adicionales aquí según la respuesta del servidor
                        } else {
                            console.log(response)
                            // Imprimir la respuesta en la consola
                            console.log('Respuesta:', response.errors);

                            let formattedErrors = '';

                            if (response.errors === 'La sesión no es válida o ha caducado, debe autenticarse nuevamente para realizar la solicitud') {
                                // Mostrar alerta de errores de validación
                                Swal.fire({
                                    icon: 'warning',
                                    title: 'Mensaje del servidor',
                                    text: response.errors,
                                    confirmButtonText: 'Aceptar'
                                }).then((result) => {
                                    // Redirigir a la página anterior al hacer clic en "Aceptar"

                                    const secretKey = 'HelloWorld2011*2024#';

                                    // Función para codificar mensajes
                                    const encodeMessage = (message) => {
                                        const ciphertext = CryptoJS.AES.encrypt(message, secretKey).toString();
                                        return encodeURIComponent(ciphertext);
                                    };

                                    // Mensaje de ejemplo
                                    const errorMessage = response.errors;

                                    // Codificar el mensaje
                                    const encodedMessage = encodeMessage(errorMessage);
                                    pag_anterior += `?error=${encodedMessage}`

                                    window.location.href = pag_anterior;
                                });
                            } else {
                                const errorMessage = response.errors;
                                console.log('Mensaje de error: ', errorMessage);

                                if (typeof errorMessage === "string" && (errorMessage.includes("campos") || errorMessage.includes("generar"))) {
                                    // Si errorMessage es una cadena que contiene "campos" o "generar"
                                    formattedErrors = errorMessage;
                                } else if (typeof errorMessage === "object") {
                                    // Si errorMessage es un objeto
                                    for (const field in errorMessage) {
                                        if (errorMessage.hasOwnProperty(field)) {
                                            formattedErrors += `${errorMessage[field][0]}\n`;
                                        }
                                    }
                                }
                                // Mostrar alerta de errores de validación
                                Swal.fire({
                                    icon: 'warning',
                                    title: 'Mensaje del servidor',
                                    text: 'Error de validación:\n' + formattedErrors,
                                    confirmButtonText: 'Aceptar'
                                });
                            }
                        }
                    },
                    error: function (error) {
                        // Ocultar el mensaje de carga y manejar errores
                        Swal.close();
                        console.error('Error al enviar el formulario:', error);
                    },
                });
            }
        });
    });
});

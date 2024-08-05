// Abre formulario de agregar entrada de reactvi
function openPopupAdd(url) {
    // Define las dimensiones y otras opciones de la ventana emergente
    var width = 800;
    var height = 600;
    var left = (window.innerWidth - width) / 2;
    var top = (window.innerHeight - height) / 2;
    var options = 'toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=' + width + ',height=' + height + ',top=' + top + ',left=' + left;

    // Abre la ventana emergente con la URL proporcionada
    window.open(url, 'popup', options);
}

//Abre formulario de Edición  registro  de reactivo

function openEditFormReact(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab/reactivos/editar_reactivo/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, '_blank', 'width=600,height=800');
}


//Abre formulario de Edición  registro de entrada de reactivo

function openEditFormIn(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab/reactivos/editar_entrada/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, '_blank', 'width=600,height=800');
}

//Abre formulario de Edición  registro de salida de reactivo

function openEditFormOut(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab/reactivos/editar_salida/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, '_blank', 'width=600,height=800');
}

//Abre formulario de Respuesta de solicitudes

function openRespondRequest(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab/solicitudes/responder_solicitud/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, '_blank', 'width=600,height=800');
}

//Abre formulario de Edición  de usuarios

function openEditFormUser(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab/usuarios/editar/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, '_blank', 'width=600,height=800');
}

// Solicitud para eliminar el registro reactivo correspondiente
function confirmDeleteUser(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: '¿Descativar Usuario',
        text: '¿Está seguro que desea eliminar el registro número:'+itemId+' "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
            var deleteUrl = '/usuarios/eliminar_usuario/' + itemId + '/';
            
            fetch(deleteUrl, {
                method: 'POST', // O el método HTTP que estés utilizando
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al eliminar el registro');
                }
            })
            .then(data => {
                icono = 'warning'

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: icono,
                    title: 'Mensaje del servidor',
                    text: data,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de eliminar
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al eliminar el registro',
                });
                location.reload();
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// Solicitud para activar el registro reactivo correspondiente
function confirmActiveUser(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Activar Usuario',
        text: '¿Está seguro que desea activar el registro número: '+itemId+' "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
            var deleteUrl = '/usuarios/activar_usuario/' + itemId + '/';
            
            fetch(deleteUrl, {
                method: 'POST', // O el método HTTP que estés utilizando
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al eliminar el registro');
                }
            })
            .then(data => {
                icono = 'warning'

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: icono,
                    title: 'Mensaje del servidor',
                    text: data,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de eliminar
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al eliminar el registro',
                });
                location.reload();
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// Solicitud para eliminar el registro reactivo correspondiente
function confirmDeleteReact(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Inactivar Reactivo',
        text: '¿Está seguro que desea eliminar el registro número: '+itemId+' "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
            var deleteUrl = '/reactivos/eliminar_reactivo/' + itemId + '/';
            
            fetch(deleteUrl, {
                method: 'POST', // O el método HTTP que estés utilizando
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al eliminar el registro');
                }
            })
            .then(data => {
                icono = 'warning'

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: icono,
                    title: 'Mensaje del servidor',
                    text: data,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de eliminar
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al eliminar el registro',
                });
                location.reload();
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// Solicitud para activar el registro reactivo correspondiente
function confirmActiveReact(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Activar Reactivo',
        text: '¿Confirma activar el registro número:'+itemId+' "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
            var deleteUrl = '/reactivos/activar_reactivo/' + itemId + '/';
            
            fetch(deleteUrl, {
                method: 'POST', // O el método HTTP que estés utilizando
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al eliminar el registro');
                }
            })
            .then(data => {
                icono = 'success'

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: icono,
                    title: 'Mensaje del servidor',
                    text: data,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de eliminar
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al activar el registro',
                });
                location.reload();
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}
// Solicitud para eliminar el registro entrada correspondiente
function confirmDeleteIn(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Eliminar Registro de entrada',
        text: '¿Está seguro que desea eliminar el registro número:'+itemId+' "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
            var deleteUrl = '/reactivos/eliminar_entrada/' + itemId + '/';
            
            fetch(deleteUrl, {
                method: 'POST', // O el método HTTP que estés utilizando
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al eliminar el registro');
                }
            })
            .then(data => {
                icono = 'warning'

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: icono,
                    title: 'Mensaje del servidor',
                    text: data,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de eliminar
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al eliminar el registro',
                });
                location.reload();
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}



// Solicitud para eliminar el registro salida correspondiente
function confirmDeleteOut(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Eliminar registro de salida',
        text: '¿Está seguro que desea eliminar el registro número:'+itemId+' "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
            var deleteUrl = '/reactivos/eliminar_salida/' + itemId + '/';
            
            fetch(deleteUrl, {
                method: 'POST', // O el método HTTP que estés utilizando
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al eliminar el registro');
                }
            })
            .then(data => {
                icono = 'warning'

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: icono,
                    title: 'Mensaje del servidor',
                    text: data,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de eliminar
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al eliminar el registro',
                });
                location.reload();
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// Solicitud para desactivar visibilidad del reactivo
function confirmHideReagent(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Ocultar Reactivo',
        text: '¿Está seguro que desea ocultar el reactivo "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
            var deleteUrl = '/UniCLab/reactivos/ocultar_reactivo/' + itemId + '/';
            
            fetch(deleteUrl, {
                method: 'POST', // O el método HTTP que estés utilizando
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al eliminar el registro');
                }
            })
            .then(data => {
                icono = 'warning'

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: icono,
                    title: 'Mensaje del servidor',
                    text: data,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de eliminar
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al eliminar el registro',
                });
                location.reload();
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}


// Solicitud para activar visibilidad del reactivo
function confirmShowReagent(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Mostrar Reactivo',
        text: '¿Está seguro que desea mostrar el reactivo "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
            var deleteUrl = '/UniCLab/reactivos/mostrar_reactivo/' + itemId + '/';
            
            fetch(deleteUrl, {
                method: 'POST', // O el método HTTP que estés utilizando
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al eliminar el registro');
                }
            })
            .then(data => {
                icono = 'warning'

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: icono,
                    title: 'Mensaje del servidor',
                    text: data,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de eliminar
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al eliminar el registro',
                });
                location.reload();
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// Solicitud para verificar disponibilidad de reactivo
function showChemicalAvailability(itemId, itemName) {
    // Realizar la solicitud AJAX directamente sin mostrar la primera alerta de confirmación
    var deleteUrl = '/UniCLab/reactivos/revisar_disponibilidad/' + itemId + '/';

    fetch(deleteUrl, {
        method: 'POST', // O el método HTTP que estés utilizando
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
        },
    })
    .then(response => {
        // Verificar el estado de la respuesta y capturar el mensaje
        if (response.ok) {
            return response.text();
        } else {
            throw new Error('Error al realizar la solicitud');
        }
    })
    .then(data => {
        // Mostrar el mensaje de éxito
        Swal.fire({
            icon: 'info',
            title: 'Mensaje del servidor',
            html: data,
        }).then(() => {
            // Recargar la página o realizar otras acciones si es necesario
            // location.reload(); // Recarga la página después de realizar la solicitud
        });
    })
    .catch(error => {
        // Manejar errores de la solicitud AJAX
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Ocurrió un error al realizar la solicitud',
        });
        // location.reload();
    });
}

// Solicitud para eliminar solicitud externa
function eliminarSolicitud(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Eliminar Solicitud',
        text: '¿Está seguro que desea eliminar la solicitud "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
            var deleteUrl = '/UniCLab/solicitudes/eliminar_solicitud_externa/' + itemId + '/';
            
            fetch(deleteUrl, {
                method: 'POST', // O el método HTTP que estés utilizando
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error al eliminar el registro');
                }
            })
            .then(data => {
                icono = 'warning'

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: icono,
                    title: 'Mensaje del servidor',
                    text: data,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de eliminar
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al eliminar el registro',
                });
                location.reload();
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}


// Solicitud para marcar solicitud como leída
function solicitudLeida(itemId, itemName) {
    // Elimina las Sweet Alerts de confirmación

    // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
    var deleteUrl = '/UniCLab/solicitudes/solicitud_leida/' + itemId + '/';
    
    fetch(deleteUrl, {
        method: 'POST', // O el método HTTP que estés utilizando
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
        },
    })
    .then(response => {
        // Verificar el estado de la respuesta y capturar el mensaje
        if (response.ok) {
            return response.text();
        } else {
            throw new Error('Error al eliminar el registro');
        }
    })
    .then(data => {
        // Cambia la confirmación del éxito por un console.log
        console.log('Mensaje del servidor:', data);

        // Recargar la página o realizar otras acciones si es necesario
        location.reload(); // Recarga la página después de eliminar
    })
    .catch(error => {
        // Manejar errores de la solicitud AJAX
        console.error('Error:', error);
        location.reload();
    });
}

// Solicitud para marcar solicitud como leída
function solicitudNoLeida(itemId, itemName) {
    // Elimina las Sweet Alerts de confirmación

    // Si el usuario hace clic en "Sí", realiza una solicitud AJAX para eliminar la entrada
    var deleteUrl = '/UniCLab/solicitudes/solicitud_no_leida/' + itemId + '/';
    
    fetch(deleteUrl, {
        method: 'POST', // O el método HTTP que estés utilizando
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de incluir el token CSRF si estás utilizando Django
        },
    })
    .then(response => {
        // Verificar el estado de la respuesta y capturar el mensaje
        if (response.ok) {
            return response.text();
        } else {
            throw new Error('Error al eliminar el registro');
        }
    })
    .then(data => {
        // Cambia la confirmación del éxito por un console.log
        console.log('Mensaje del servidor:', data);

        // Recargar la página o realizar otras acciones si es necesario
        location.reload(); // Recarga la página después de eliminar
    })
    .catch(error => {
        // Manejar errores de la solicitud AJAX
        console.error('Error:', error);
        location.reload();
    });
}

// -------------------------------------------------------- //
// Abre formulario de Edición  de clasificación de residuos //

function openEditFormClass(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab_Residuos/Clasificacion_Residuos/Editar/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, '_blank', 'width=600,height=800');
}


// --------------------------------------------------- //
// Función para inactivar la clasificación de residuos //

function disableWasteSorting(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Deshabilitar Clasificación',
        text: '¿Está seguro que desea desactivar la clasificación "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Clasificacion_Residuos/Desactivar/' + itemId + '/';  // Ruta de la vista de desactivación

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al desactivar la clasificación');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// --------------------------------------------------- //
// Función para activar la clasificación de residuos //

function enableWasteSorting(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Habilitar Clasificación',
        text: '¿Está seguro que desea activar la clasificación "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Clasificacion_Residuos/Activar/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// ---------------------------------------------------- //
// Abre formulario de Edición  de resgistro de residuos //

function openEditFormRecordWaste(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab_Residuos/Registro_Residuos/Editar/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, '_blank', 'width=600,height=800');
}

// ---------------------------------------------- //
// Función para deshabilitar registro de residuos //

function disableWasteRecord(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Deshabilitar Registro',
        text: '¿Está seguro que desea desactivar el registro de residuo "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Registro_Residuos/Desactivar/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// ---------------------------------------------- //
// Función para habilitar registro de residuos //

function enableWasteRecord(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Habilitar Registro',
        text: '¿Está seguro que desea activar el registro de residuo "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Registro_Residuos/Activar/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// --------------------------------------------------- //
// Función para eliminar residuos de la lista temporal //
function deleteWaste(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Eliminar Registro',
        text: '¿Está seguro que desea eliminar de la lista el residuo '+itemName+'?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Por favor espere...',
                html: 'Enviando datos al servidor',
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Registro_Residuos/Eliminar/'+itemId+'/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Ocultar el loader
                Swal.hideLoading();

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Ocultar el loader
                Swal.hideLoading();

                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        }
    });
}




// Función para enviar registro de residuos //
function sendInfoWasteRecord() {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Enviar Información',
        text: '¿Está seguro que enviar la solicitud?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Por favor espere...',
                html: 'Enviando datos al servidor',
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Registro_Residuos/Enviar_Solicitud/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Ocultar el loader
                Swal.hideLoading();

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Ocultar el loader
                Swal.hideLoading();

                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        }
    });
}


// ------------------------------------------------------------- //
// Función para cancelar toda la soolicitud registro de residuos //
function cancelInfoWasteRecord() {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Cancelar envío de Información',
        text: '¿Está seguro que cancelar la solicitud?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Por favor espere...',
                html: 'Enviando datos al servidor',
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Registro_Residuos/Cancelar_Solicitud/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Ocultar el loader
                Swal.hideLoading();

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Ocultar el loader
                Swal.hideLoading();

                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        }
    });
}



// ------------------------------------------------------------- //
// Función para cancelar toda la soolicitud registro de residuos //
function DeleteWasteRecord(itemId,itemName, itemSol) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Eliminar Registro de la solicitud '+itemSol,
        text: '¿Está seguro que desea eliminar el registro de residuo '+itemName+'?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Por favor espere...',
                html: 'Enviando datos al servidor',
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Registro_Residuos/Eliminar_Registro/'+itemId+'/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Ocultar el loader
                Swal.hideLoading();

                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Ocultar el loader
                Swal.hideLoading();

                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        }
    });
}
// ---------------------------------------------------- //
// Abre vista de detalle de Solicitud de residuos //

function openDetailRecordWaste(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab_Residuos/Registro_Residuos/Solicitudes/Ver/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, 'popupWindow', 'width=1280, height=800,menubar=no,toolbar=no,location=no,status=no,resizable=no');
    

}


// ------------------------------------------------------------- //
// Función para cancelar toda la solicitud de registro de residuos //
function MarkAsUnreadWasteRecord(itemId) {
    Swal.fire({
        title: 'Enviando',
        html: 'Por favor espere...',
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading();
        },
        showConfirmButton: false // Ocultar el botón "Aceptar"
    });

    // Realiza una solicitud AJAX
    var deactivateUrl = '/UniCLab_Residuos/Registro_Residuos/No_leido/' + itemId + '/';  // Ruta de la vista de acción

    fetch(deactivateUrl, {
        method: 'POST', // Método HTTP POST
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
        },
    })
    .then(response => {
        // Verificar el estado de la respuesta y capturar el mensaje
        if (response.ok) {
            return response.json();  // Leer los datos JSON de la respuesta
        } else {
            throw new Error('Error al ejecutar la acción');
        }
    })
    .then(data => {
        // Mostrar el mensaje de éxito en la consola
        console.log('Mensaje del servidor:', data.message);

        // Cerrar el loader
        Swal.close();

        // Recargar la página o realizar otras acciones si es necesario
        location.reload(); // Recarga la página después de desactivar la clasificación
    })
    .catch(error => {
        // Ocultar el loader y mostrar un error
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.message,
        });
    });
}

// ---------------------------------------------------- //
// Abre vista de Edición de ficha de seguridad de residuos //

function openEditSecuritySheet(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab_Residuos/Fichas_Seguridad/Editar/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, 'popupWindow', 'width=1280, height=800,menubar=no,toolbar=no,location=no,status=no,resizable=no');
    

}

// ---------------------------------------------- //
// Función para deshabilitar fichas de seguirdad //

function disableSecuritySheet(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Deshabilitar Registro',
        text: '¿Está seguro que desea desactivar ela ficha de seguridad "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Fichas_Seguridad/Desactivar/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// ---------------------------------------------- //
// Función para habilitar fichas de seguirdad //

function enableSecuritySheet(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Habilitar Registro',
        text: '¿Está seguro que desea activar la ficha de seguridad "' + itemName + '"?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Fichas_Seguridad/Activar/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}


// ---------------------------------------------------- //
// Abre vista de Edición de Certificado de disposición de residuos //

function openEditFinalCertificate(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab_Residuos/Certificados_Disposicion/Editar/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, 'popupWindow', 'width=1280, height=800,menubar=no,toolbar=no,location=no,status=no,resizable=no');
    

}

// ----------------------------------------------------- //
// Función para deshabilitar certificados de disposición //

function disableFinalCertificateDisposition(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Dehabilitar Registro',
        text: '¿Realmente desea deshabilitar el certificado de disposición final?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Certificados_Disposicion/Deshabilitar/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}


// ----------------------------------------------------- //
// Función para deshabilitar certificados de disposición //

function enableFinalCertificateDisposition(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Habilitar Registro',
        text: '¿Realmente desea habilitar el certificado de disposición final?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Certificados_Disposicion/Habilitar/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}


// ---------------------------------------------------- //
// Abre vista de Edición de Material de interés //

function openEditImportantLink(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab_Residuos/Enlaces_Interes/Editar/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, 'popupWindow', 'width=1280, height=800,menubar=no,toolbar=no,location=no,status=no,resizable=no');
    

}

// ----------------------------------------------------- //
// Función para deshabilitar material de interés //

function disableImportantLink(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Dehabilitar Registro',
        text: '¿Realmente desea deshabilitar este material de interés?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Enlaces_Interes/Deshabilitar/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// ----------------------------------------------------- //
// Función para habilitar material de interés //

function enableImportantLink(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Habilitar Registro',
        text: '¿Está seguro de deshabilitar este material de interés?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab_Residuos/Enlaces_Interes/Habilitar/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}

// ------------------------------------ //
// Abre vista de Edición de Pictogramas //

function openEditPictogram(itemId) {
    // Construye la URL del formulario de edición con el ID del elemento
    var editUrl = '/UniCLab/Etiquetas/Editar_Pictograma/' + itemId + '/';

    // Abre una nueva ventana emergente con el formulario de edición
    window.open(editUrl, 'popupWindow', 'width=1280, height=800,menubar=no,toolbar=no,location=no,status=no,resizable=no');
    

}


// ------------------------- //
// Desactivar de Pictogramas //

function disablePictogram(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Deshabilitar Registro',
        text: '¿Realmente desea deshabilitar este Pictograma?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab/Etiquetas/Inhabilitar_Pictograma/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}
// ---------------------- //
// Activar de Pictogramas //
function enablePictogram(itemId, itemName) {
    // Muestra una Sweet Alert de confirmación
    Swal.fire({
        title: 'Habilitar Registro',
        text: '¿Realmente desea habilitar este Pictograma?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario hace clic en "Sí", realiza una solicitud AJAX 
            var deactivateUrl = '/UniCLab/Etiquetas/Habilitar_Pictograma/' + itemId + '/';  // Ruta de la vista de acción

            fetch(deactivateUrl, {
                method: 'POST', // Método HTTP POST
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Incluir el token CSRF si se utiliza Django
                },
            })
            .then(response => {
                // Verificar el estado de la respuesta y capturar el mensaje
                if (response.ok) {
                    return response.json();  // Leer los datos JSON de la respuesta
                } else {
                    throw new Error('Error al ejecutar la acción');
                }
            })
            .then(data => {
                // Mostrar el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Mensaje del servidor',
                    text: data.message,
                }).then(() => {
                    // Recargar la página o realizar otras acciones si es necesario
                    location.reload(); // Recarga la página después de desactivar la clasificación
                });
            })
            .catch(error => {
                // Manejar errores de la solicitud AJAX
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            });
        } else {
            // Si el usuario hace clic en "No", cierra la Sweet Alert
            Swal.close();
        }
    });
}
// ------------------------------------------------- //
// Función para obtener el token CSRF de las cookies //
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Buscar el nombre de la cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



document.addEventListener('DOMContentLoaded', function () {
    const tipoField = document.getElementById('id_tipo');
    const urlField = document.getElementById('id_url');
    const urlError = document.getElementById('url-error');

    // Función para visibilizar URL
    function toggleUrlField() {
        if (tipoField.value === 'Video de Youtube') {
            urlField.placeholder = 'Ejemplo: https://www.youtube.com/watch?v=kuvJNJ9dGJk&list';
            urlField.value = '';
            urlField.parentElement.style.display = 'block';
            urlError.style.display = 'none'; // Ocultar el mensaje de error
        } else if (tipoField.value === 'Enlace Externo') {
            urlField.placeholder = 'Ejemplo: https://www.manizales.unal.edu.co/';
            urlField.value = '';
            urlField.parentElement.style.display = 'block';
            urlError.style.display = 'none'; // Ocultar el mensaje de error
        } else {
            urlField.value = '';
            urlField.parentElement.style.display = 'none';
            urlError.style.display = 'none'; // Ocultar el mensaje de error
        }
    }

    // Función para prevalidar el campo de URL
    function validateUrl() {
        const urlValue = urlField.value.trim();
        urlError.textContent = ''; // Limpiar cualquier mensaje de error previo
        urlError.style.display = 'none'; // Ocultar el mensaje de error por defecto
        if (urlValue !== '') {
            if (tipoField.value === 'Video de Youtube') {
                const youtubePattern = /^(https?:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$/;
                if (!youtubePattern.test(urlValue)) {
                    urlError.textContent = 'El enlace no cumple con las especificaciones de un enlace de YouTube.';
                    urlError.style.display = 'block'; // Mostrar el mensaje de error
                }
            } else if (tipoField.value === 'Enlace Externo') {
                try {
                    new URL(urlValue); // Valida si es una URL válida
                } catch (e) {
                    urlError.textContent = 'El enlace no cumple con las especificaciones de una URL válida.';
                    urlError.style.display = 'block'; // Mostrar el mensaje de error
                }
            }
        }
    }

    // Evento del campo tipo
    tipoField.addEventListener('change', toggleUrlField);

    // Event listener para prevalidar el campo de URL al perder el enfoque
    urlField.addEventListener('blur', validateUrl);
    // cargar la función al inicio
    toggleUrlField();
});
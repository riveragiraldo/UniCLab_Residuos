document.addEventListener('DOMContentLoaded', function () {
    var checkboxFormatoLibre = document.getElementById('empty_template');
    var botonLimpiar = document.querySelector('button[type="reset"]');
    var botonGenerar = document.querySelector('button[type="submit"]');
    var linkDescargar = document.getElementById('download_link');
    var form = document.getElementById('label_substances_form');

    // Función para deshabilitar elementos específicos por id
    function deshabilitarElementos(ids) {
        ids.forEach(function (id) {
            var element = document.getElementById(id);
            if (element) {
                element.setAttribute('disabled', 'disabled');
                element.value = ''; // Limpiar el valor del campo
            }
        });
    }

    // Función para habilitar elementos específicos por id
    function habilitarElementos(ids) {
        ids.forEach(function (id) {
            var element = document.getElementById(id);
            if (element) {
                element.removeAttribute('disabled');
            }
        });
    }

    // Al cargar la página, verificar estado inicial del checkbox
    if (checkboxFormatoLibre.checked) {
        deshabilitarElementos(['keyword', 'number', 'reagent', 'cas', 'id_reagent', 'lab', 'ID_Hermes', 'emergency_number']);
        deshabilitarElementos(['label_type1', 'label_type2', 'label_type3', 'label_type4']);
        botonLimpiar.setAttribute('disabled', 'disabled');
        botonGenerar.classList.add('hidden');
        linkDescargar.classList.remove('hidden');
    }

    // Detectar cambios en el checkbox
    checkboxFormatoLibre.addEventListener('change', function () {
        if (this.checked) {
            deshabilitarElementos(['keyword', 'number', 'reagent', 'cas', 'id_reagent', 'lab', 'ID_Hermes', 'emergency_number']);
            deshabilitarElementos(['label_type1', 'label_type2', 'label_type3', 'label_type4']);
            botonLimpiar.setAttribute('disabled', 'disabled');
            botonGenerar.classList.add('hidden');
            linkDescargar.classList.remove('hidden');
        } else {
            habilitarElementos(['keyword', 'number', 'reagent', 'cas', 'id_reagent', 'lab', 'ID_Hermes', 'emergency_number']);
            habilitarElementos(['label_type1', 'label_type2', 'label_type3', 'label_type4']);
            botonLimpiar.removeAttribute('disabled');
            botonGenerar.classList.remove('hidden');
            linkDescargar.classList.add('hidden');
        }
    });

    // Al cargar la página, asegurarse de que el botón Limpiar esté habilitado inicialmente
    botonLimpiar.removeAttribute('disabled');
});

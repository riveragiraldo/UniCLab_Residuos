document.addEventListener("DOMContentLoaded", function () {
    // Obtener elementos del DOM
    var dependenciaSelect = document.getElementById('id_dependencia');
    var areaContainer = document.getElementById('area-container');
    var laboratorioContainer = document.getElementById('lab-container');
    var laboratorio = document.getElementById('id_laboratorio')
    var area = document.getElementById('id_area')

    // Función para actualizar la visibilidad y los atributos requeridos según el valor de 'Dependencia'
    function actualizarVisibilidad() {
        var dependenciaValue = dependenciaSelect.value;

        if (dependenciaValue === '') {
            areaContainer.style.display = 'none';
            laboratorioContainer.style.display = 'none';
            laboratorio.removeAttribute('required');
            area.removeAttribute('required');
        } else if (dependenciaValue === 'Area') {
            areaContainer.style.display = 'block';
            laboratorioContainer.style.display = 'none';
            laboratorio.removeAttribute('required');
            area.setAttribute('required', '');
        } else if (dependenciaValue === 'Laboratorio') {
            areaContainer.style.display = 'none';
            laboratorioContainer.style.display = 'block';
            area.removeAttribute('required');
            laboratorio.setAttribute('required', '');
        } else {
            areaContainer.style.display = 'none';
            laboratorioContainer.style.display = 'none';
            aboratorio.removeAttribute('required');
            area.removeAttribute('required');
        }
    }

    // Llamar a la función de actualización al cargar la página
    actualizarVisibilidad();

    // Agregar un evento de cambio al selector de 'Dependencia'
    dependenciaSelect.addEventListener('change', function () {
        actualizarVisibilidad();
    });




    // Función para seleccionar la opción en el selector de estado por su nombre
    function seleccionarOpcionPorNombre(selector, nombreOpcion) {
        var options = selector.options;
        for (var i = 0; i < options.length; i++) {
            if (options[i].text.toLowerCase() === nombreOpcion.toLowerCase()) {
                selector.selectedIndex = i;
                break;
            }
        }
    }

    // Función para ajustar el estado según las unidades seleccionadas
    function ajustarEstado() {
        var unidadesSelector = document.getElementById('id_unidades')
        var estadoSelector = document.getElementById('id_estado');

        // Obtener el valor seleccionado en el selector de unidades (en minúsculas)
        var unidadesSeleccionadas = unidadesSelector.options[unidadesSelector.selectedIndex].text.toLowerCase();
        

        // Verificar las unidades seleccionadas y ajustar el estado en consecuencia
        if (unidadesSeleccionadas === 'g' || unidadesSeleccionadas === 'mg' || unidadesSeleccionadas === 'kg') {
            // estadoSelector.disabled = true; // Deshabilitar el selector
            // Si las unidades son g, mg o Kg, establecer el estado en SOLIDO
            seleccionarOpcionPorNombre(estadoSelector, 'SOLIDO'); // Valor para SOLIDO
        } else if (unidadesSeleccionadas === 'l' || unidadesSeleccionadas === 'ml' || unidadesSeleccionadas === 'cc'|| unidadesSeleccionadas === 'gal') {
            //estadoSelector.disabled = true; // Deshabilitar el selector
            // Si las unidades son l, ml o cc, establecer el estado en LIQUIDO
            seleccionarOpcionPorNombre(estadoSelector, 'LIQUIDO'); // Valor para LIQUIDO
        } else {
            // No hacer cambios si las unidades no coinciden con las mencionadas
            //estadoSelector.disabled = false; // Deshabilitar el selector
            seleccionarOpcionPorNombre(estadoSelector, '---------'); // Valor inicial
        }

    }

    // Agregar un event listener para el cambio en el selector de unidades
    var unidadesSelector = document.getElementById('id_unidades');
    unidadesSelector.addEventListener('change', function () {
        // Esperar 50ms antes de ajustar el estado
        setTimeout(ajustarEstado, 50);
    });

    // Llamar a la función al cargar la página para ajustar el estado inicialmente
    ajustarEstado();


    


});

// Función para abrir ventane emergente de listado de clasificaciones
function openPopup(url) {
    // Definir las dimensiones de la ventana emergente
    var width = 600;
    var height = 400;
    // Calcular la posición del centro de la pantalla
    var left = (screen.width - width) / 2;
    var top = (screen.height - height) / 2;
    // Abrir la ventana emergente
    window.open(url, '_blank', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, copyhistory=no, width=' + width + ', height=' + height + ', top=' + top + ', left=' + left);
    return false;
}

//autocompletar por nombre o código
//Envía valores escritos en el campo name a la vista AutocompleteOutAPI, esta devuelve los valores de code cas y name, se concatenan y 
//se visualizan en forma de lista desplegable 
$(document).ready(function () {
    $("#keyword").autocomplete({
        source: "/UniCLab/Etiquetas/Automcompletar_Sustancias/",
        minLength: 2,
        select: function (event, ui) {
            // Obtener el Nombres del objeto seleccionado
            var name = ui.item.name;
            var cas = ui.item.cas;
            var id_substance = ui.item.id_substance;

            // Concatenar el Nombres en un formato deseado
            var optionLabel = name + " - " + cas;

            // Establecer el valor y la etiqueta del campo de entrada
            $("#keyword").val(optionLabel);
            $("#id_reagent").val(id_substance);
            $("#reagent").val(name);
            $("#cas").val(cas);
       
            return false;
        },
        focus: function (event, ui) {
            // Prevenir la actualización del valor del campo de entrada al enfocar una opción
            event.preventDefault();
        },
        response: function (event, ui) {
            // Manipular la respuesta antes de mostrar las opciones
            ui.content.forEach(function (item) {
                
                item.label = item.name + " - " + item.cas;
                item.value = item.name;  // Establecer el valor de la opción como el nombre
                
            });
        }
    });
});



$(document).ready(function () {
    $('#name').autocomplete({
        source: function (request, response) {
            var term = request.term;
            


            $.getJSON('/UniCLab/Etiquetas/Automcompletar_Sustancias/', { term: term})
                .done(function (data) {
                    response(data);
                });
        },
        select: function (event, ui) {
            // Obtener el NOmbres del objeto seleccionado
            var name = ui.item.name;
            var cas = ui.item.name;
            var id_substance = ui.item.id_substance;

            // Concatenar el Nombres en un formato deseado
            var optionLabel = name+" - "+cas;

            // Establecer el valor y la etiqueta del campo de entrada
            $("#keyword").val(optionLabel);
            $("#reagent").val(name);
            $("#id_reagent").val(id_substance);

            // Evento blur para verificar y corregir el campo name
            $('#keyword').on('blur', function () {
                var currentValue = $(this).val();
                nombreAnterior = optionLabel
                // Si el campo name se borra, también borra #id_user
                if (currentValue !== "") {



                if (currentValue !== nombreAnterior) {
                    // Si el valor actual no coincide con la opción autocompletada
                    $(this).val(nombreAnterior); // Corrige el valor
                }
            }else{
                $("#id_reagent").val("");
            }
        });

    
},
    minLength: 2

    });

});







// Añadir eventos de click a los enlaces externos después de que la alerta se muestre
document.querySelectorAll('.external-link').forEach(link => {
    link.addEventListener('click', function (event) {
        event.preventDefault(); // Prevenir la acción por defecto del enlace
        const url = this.href;
        mostrarAlertaJavaScript(url);
    });
});

// Función para mostrar una alerta normal de JavaScript
function mostrarAlertaJavaScript(url) {
    const mensaje = `\nSaliendo UniCLab Residuos...\n\nLa Dirección de Laboratorios de la Universidad Nacional de Colombia sede Manizales como dependencia gestora del software UniClab, no se hace responsable por la calidad y pertinencia de los contenidos de webs ajenas a esta.\n\n¿Desea continuar?\n`;
    if (confirm(mensaje)) {
        window.open(url, '_blank');
    }
}
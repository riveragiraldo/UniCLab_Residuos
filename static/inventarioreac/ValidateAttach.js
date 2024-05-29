document.getElementById('id_attach').addEventListener('change', function () {
    const fileInput = this;
    const file = fileInput.files[0];
    const maxSize = 2 * 1024 * 1024; // 2MB
    const allowedExtensions = /(\.pdf)$/i;
    const errorDiv = document.getElementById('file-error');

    if (file) {
        // Check file size
        if (file.size > maxSize) {
            errorDiv.style.display = 'block';
            errorDiv.textContent = 'El tamaño máximo del archivo es 2MB. No se adjunto ningún archivo';
            fileInput.value = ''; // Clear the input
            return;
        }

        // Check file extension
        if (!allowedExtensions.exec(file.name)) {
            errorDiv.style.display = 'block';
            errorDiv.textContent = 'Solo se permiten archivos con extensiones .pdf. No se adjunto ningún archivo';
            fileInput.value = ''; // Clear the input
            return;
        }

        // Clear any previous error messages
        errorDiv.style.display = 'none';
        errorDiv.textContent = '';
    }
});
// Inicializar Signature Pad y asociarlo con el lienzo
const canvas = document.getElementById('pizarra');
const signaturePad = new SignaturePad(canvas);
const nombreEmpleado = empleado;
function aparecerPizarra() {
    // Mostrar el elemento con id="pizarraFirma"
    document.getElementById("pizarraFirma").style.display = "flex";
    // Ocultar el botón con id="BotGenerar"
    document.getElementById("BotGenerar").style.display = "none";
}

// Función para borrar la firma
function borrarFirmar() {
    signaturePad.clear();
}

// Función para guardar la firma como PNG
function guardarFirmar() {
    // Comprobar si hay algo dibujado en el lienzo
    if (!signaturePad.isEmpty()) {
        // Obtener la fecha y hora actual
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');

        // Construir el nombre del archivo
        const fileName = `Empleado_${nombreEmpleado}_${year}_${month}_${day}_${hours}:${minutes}:${seconds}.png`;
        // Obtener la firma como datos URL en formato PNG
        const dataURL = signaturePad.toDataURL('image/png');
        // Crear un enlace de descarga y activarlo para descargar la firma
        const link = document.createElement('a');
        link.download = fileName;
        link.href = dataURL;
        link.click();
        // Ocultar los botones después de guardar la firma
        document.getElementById("BotBorrar").style.display = "none";
        document.getElementById("BotGuardarF").style.display = "none";
        
        // Deshabilitar la capacidad de dibujar en el lienzo
        signaturePad.off(); 
    } else {
        alert("No hay firma para guardar.");
    }
}

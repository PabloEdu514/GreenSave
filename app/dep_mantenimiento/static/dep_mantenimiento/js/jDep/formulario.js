// Inicializar Signature Pad y asociarlo con el lienzo
const canvas = document.getElementById('pizarra');
const signaturePad = new SignaturePad(canvas);

// Función para borrar la firma
function borrarFirmar() {
    signaturePad.clear();
}

// Función para guardar la firma como PNG
function guardarFirmar() {
    // Comprobar si hay algo dibujado en el lienzo
    if (!signaturePad.isEmpty()) {
        // Obtener la firma como datos URL en formato PNG
        const dataURL = signaturePad.toDataURL('image/png');
        // Crear un enlace de descarga y activarlo para descargar la firma
        const link = document.createElement('a');
        link.download = 'firma.png';
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
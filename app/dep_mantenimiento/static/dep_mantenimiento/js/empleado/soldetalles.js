// soldetalles.js

// Esperar a que el DOM se cargue completamente para asegurar que el botón esté disponible
document.addEventListener('DOMContentLoaded', (event) => {
    // Obtener el botón por su ID
    const botonInicio = document.getElementById('BotInicio');
    
    // Obtener la URL del elemento script con el ID user-data
    const urlInicio = document.getElementById('url-inicio').getAttribute('data-url-inicio');

    // Asignar la función volverInicio al evento de clic del botón
    if (botonInicio) {
        botonInicio.addEventListener('click', () => {
            window.location.href = urlInicio;
        });
    }
});


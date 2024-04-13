//home.js
$(document).ready(function(){
   
    // Obtener el botón de recargar
    var botonRecargar = document.getElementById("recargar");

    // Agregar un evento de clic al botón
    botonRecargar.addEventListener("click", function() {
        // Mostrar una alerta cuando se hace clic en el botón
        alert("Tabla de solicitudes recargada");
    });



    // Manejador de clic para el botón "Eliminar"
    $("#Eliminar").click(function(event){
        event.stopPropagation(); // Evitar que el evento se propague a la fila
        eliminar(); // Llamar a la función eliminar()
    });
    
    // Manejador de clic para el botón "Editar"
    $("#boton-editar").click(function(event) {
        event.stopPropagation(); // Evitar que el evento se propague a la fila
        alert("Haz hecho clic en el botón Editar. Puede editar el elemento aquí.");
    });
    
        // Manejador de clic para la fila 1
    $(".fila-1").click(function(){
        alert("Haz hecho clic en la fila 1");
    });

    // Manejador de clic para la fila 2
    $(".fila-2").click(function(){
        alert("Haz hecho clic en la fila 2");
    });

    // Manejador de clic para la fila 3
    $(".fila-3").click(function(){
        alert("Haz hecho clic en la fila 3");
    });

   


});

function eliminar() {
    alert("¡Solicitud eliminada correctamente!");
}


$(document).ready(function() {
    // Delegar eventos de clic a los botones "Editar" y "Eliminar" dentro de la tabla
    $('#Solicitudes').on('click', '.editar-btn', function() {
        // Redirigir a la URL de edición
        window.location.href = "";
    });

    $('#Solicitudes').on('click', '.eliminar-btn', function() {
        // Obtener el ID de la solicitud que se va a eliminar
        var solicitudId = $(this).data('solicitud-id');

        // Mostrar un mensaje de confirmación
        if (confirm("¿Estás seguro de que deseas eliminar esta solicitud?")) {
            // Si el usuario confirma la eliminación, enviar una solicitud AJAX para eliminar la solicitud
            $.ajax({
                url: '/eliminar-solicitud/',  // URL de la vista que maneja la eliminación de la solicitud
                type: 'POST',  // Método HTTP para enviar la solicitud
                data: {
                    solicitud_id: solicitudId  // Enviar el ID de la solicitud a eliminar
                },
                success: function(response) {
                    // Si la solicitud se elimina con éxito, actualizar la tabla o recargar la página
                    // Por ejemplo, podrías recargar la página completa o eliminar la fila de la tabla
                    // correspondiente a la solicitud eliminada
                    // window.location.reload();  // Recargar la página completa
                    // $(this).closest('tr').remove();  // Eliminar la fila de la tabla
                    alert("La solicitud se eliminó con éxito.");
                },
                error: function(xhr, errmsg, err) {
                    // Si ocurre un error al eliminar la solicitud, mostrar un mensaje de error
                    console.log(xhr.status + ": " + xhr.responseText);
                    alert("Se produjo un error al intentar eliminar la solicitud.");
                }
            });
        }
    });

    // Agregar el evento de clic para expandir la descripción
    $(document).on('click', '.columna-descripcion', function() {
        // Cambiar el estilo para mostrar todo el texto al hacer clic
        $(this).css('white-space', 'normal');
        $(this).css('overflow', 'visible');
        $(this).css('text-overflow', 'inherit');
    });
});

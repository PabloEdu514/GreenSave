document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("btnEnviar").addEventListener("click", function() {
        
        var material = document.getElementById("id_material_Asignado").value;
        
        var mensaje = "¿Estás seguro de que estos son los materiales necesarios?<br><br>";
      
        mensaje += "<strong>Material a utilizar:</strong> " + material + "<br>";
        
        Swal.fire({
            title: 'Confirmación',
            html: mensaje,
            icon: 'question',
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            confirmButtonText: 'Aceptar',
        }).then((result) => {
            if (result.isConfirmed) {
                document.getElementById("miFormulario").submit();
            }
        });
    });

    
});

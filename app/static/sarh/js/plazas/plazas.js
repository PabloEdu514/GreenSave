$(document).ready(function() {
    getPlazas();
    getHistorial();
});

function getPlazas() {
    $("#tablaPlazas").DataTable({
        "responsive": true,
        "lengthChange": false,
        "autoWidth": true,
        "buttons": ["copy", "csv", "excel", "pdf", "print"]

    }).buttons().container().appendTo('#tablaPlazas_wrapper .col-md-6:eq(0)');
}

function getHistorial() {
    $("#tablaHistorial").DataTable({
        "responsive": true,
        "lengthChange": false,
        "autoWidth": true,
        "buttons": ["copy", "csv", "excel", "pdf", "print"]

    }).buttons().container().appendTo('#tablaHistorial_wrapper .col-md-6:eq(0)');
}


function validateEditarFormJustificacion() {

    let id_tipo = jQuery('#id_tipo_plaza').val();
    let id_plaza = jQuery('#id_plaza_plaza').val();
    let id_efectos = jQuery('#id_efectos').val();

    var validate = true;
    if (id_tipo === "") {
        validate = false;
    }
    if (id_plaza === "") {
        validate = false;
    }

    if (id_efectos === "") {
        validate = false;
    }
    return validate;
}

$('#editPlaza').on('click', function(e) {
    e.preventDefault();
    if (validateEditarFormJustificacion()) {
        let formData = {
            tipo: jQuery('#id_tipo_plaza').val(),
            plaza: jQuery('#id_plaza_plaza').val(),
            efectos: jQuery('#id_efectos').val(),
        };

        console.log(formData)

        $.ajax({
            url: "/sarh/editarplaza",
            data: formData,
            method: "POST",
            async: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            mode: 'same-origin',
            success: function(data) {
                if (data) {
                    Swal.fire({
                        text: data.name,
                        icon: 'success',
                        confirmButtonText: 'Cool'
                    })
                    getPlazas()
                }
            },
            error: function(error) {
                Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                        confirmButtonText: 'Cool'
                    })
            }
        });
    } else {
        Swal.fire({
                        text: "Todos los campos son necesarios",
                        icon: 'error',
                        confirmButtonText: 'Cool'
                    })
    }
});

$('#savePlaza').on('click', function(e) {
    e.preventDefault();
    if (validateFormPlaza()) {

        let formData = {
            id: jQuery('#plaza_historial_editar').val(),
            plaza: jQuery('#plaza_plaza_editar').val(),
            tipo: jQuery('#plaza_tipo_editar').val(),
            inicia: jQuery('#plaza_init_editar').val(),
            termina: jQuery('#plaza_termina_editar').val(),
            trabajador: jQuery('#plaza_trabajador_editar').val(),
        };
        console.log(formData)
        $.ajax({
            url: "/sarh/editarPlaza",
            data: formData,
            method: "POST",
            async: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            mode: 'same-origin',
            success: function(data) {
                if (data) {
                    Swal.fire({
                        text: data.name,
                        icon: 'success',
                        confirmButtonText: 'Cool'
                    })
                    //getHistorial()
                    location.reload()
                }
            },
            error: function(error) {
                Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                        confirmButtonText: 'Cool'
                    })
            }
        });
    } else {
        Swal.fire({
                        text: "Todos los campos son necesarios",
                        icon: 'error',
                        confirmButtonText: 'Cool'
                    })
    }
});

function validateFormPlaza() {
    let id_tipo = jQuery('#plaza_tipo').val();
    let id_inicia = jQuery('#plaza_inicia').val();
    let id_termina = jQuery('#plaza_termina').val();
    let id_trabajador = jQuery('#plaza_trabajador_edita').val();
    var validate = true;
    if (id_tipo === "") {
        validate = false;
    }
    if (id_inicia === "") {
        validate = false;
    }
    if (id_termina === "") {
        validate = false;
    }
    if (id_trabajador === "") {
        validate = false;
    }
    if (id_inicia > id_termina) {
        validate = false;
    }
    return validate;
}

function getRecordPlaza(id) {

    let formData = {
        id: id,
    };

    $.ajax({
        url: "/sarh/getrecordPlaza",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data) {

                $("#plaza_tipo_editar").val(data.tipo).change();
                $("#plaza_termina_editar").val(formatDate(data.termina)).change();
                $("#plaza_historial_editar").val(data.id).change();
                $("#plaza_plaza_editar").val(data.plaza).change();
                $("#plaza_trabajador_editar").val(data.trabajador).change();
                $("#efectos").val(data.efectos).change();
                $("#plaza_init_editar").val(formatDate(data.termina)).change();

            }
        },
        error: function(error) {
            console.log(error);
        }
    });

}

function eliminarplazas(id) {
    $("#eliminar_plaza").val(id).change();
}

//Método para eliminarPlazas
$('#eliminarPlaz').on('click', function(e) {
    e.preventDefault();

    let formData = {
        id: jQuery('#eliminar_plaza').val()
    };

    console.log(FormData)

    $.ajax({
        url: "/sarh/eliminarplazas",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data) {
                Swal.fire({
                        text: data.name,
                        icon: 'success',
                        confirmButtonText: 'Cool'
                    })
                location.reload();
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                        confirmButtonText: 'Cool'
                    })
        }
    });
});
var globalTrabajadorId, globalIncidenciaId, globalRenglon;

$(document).ready(function () {
    //alert('hola');
});

function createJustificante(fecha, tipoInc, idTrabajador, incId, ren) {
    nuevaFecha = fecha.substring(6) + '-' + fecha.substring(3, 5) + '-' + fecha.substring(0, 2)
    globalTrabajadorId = idTrabajador;
    globalIncidenciaId = incId;
    globalRenglon = ren;
    //Fecha del justificante
    document.getElementById("id_FechaJust").value = nuevaFecha;
    document.getElementById("id_FechaJust").disabled = true;
    //Tipo de justificante
    switch (tipoInc) {
        case 'EA':
        case 'R2':
        case 'R1':
        case 'FR':
            document.getElementById("id_TipoJust").value = 'E';
            document.getElementById("id_TipoJust").disabled = true;
            break;
        case 'FT':
            document.getElementById("id_TipoJust").value = 'D';
            document.getElementById("id_TipoJust").disabled = true;
            break;
        case 'SP':
        case 'OS':
        case 'SA':
            document.getElementById("id_TipoJust").value = 'S';
            document.getElementById("id_TipoJust").disabled = true;
    }
}

function modificarTabla() {
    var tablinga = $('#tablaDeIncidencias').dataTable();
    //1) Valor a meter
    //2) Renglon donde se mete
    //3) Columna donde se mete
    //4) Para no recargar la tabla
    //NOTA: Para editar un renglon completo ver subirRegistrosHuella.js
    tablinga.fnUpdate('<p style="color: green;">Justificada</p>', globalRenglon, 6, false);
    meter = ` <ul class="navbar-nav" onclick="getRegXDia({{incidencia.id}})" title="Ver registros del día">
    <li class="nav-item">
        <a class="nav-link {% if 'index' in segment %} active {% endif %} dropdown-toggle d-flex align-items-center"
            href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            <div
                class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12"
                    fill="currentColor" class="bi bi-clock-fill" viewBox="0 0 16 16">
                    <path
                        d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z" />
                </svg>
            </div>
        </a>
        <ul class="dropdown-menu dropdown-menu-dark p-1" id="{{incidencia.id}}">
        </ul>
    </li>
</ul>

<button type="button" disabled class="btn btn-primary" title="Agregar Justificante"
onclick="createJustificante('{{incidencia.fecha|date:'SHORT_DATE_FORMAT'}}', '{{incidencia.incidencia.clave}}', '{{incidencia.trabajador.id}}', '{{incidencia.id}}', '{{forloop.counter0}}')"
data-bs-toggle="modal" data-bs-target="#modalCrearJustificante">
<i class="fas fa-plus fa-sm"></i>
</button> `
    tablinga.fnUpdate(meter, globalRenglon, 7, false);
}

//Método para guardar alguna justificacion
$('#saveJustificante').on('click', function (e) {
    e.preventDefault();
    if (validateFormJustificaion()) {
        var b = new Boolean(false);
        if (jQuery('#id_MedicoJust').val() == "true")
            b = true
        let formData = {
            fecha: jQuery('#id_FechaJust').val(),
            tipo: jQuery('#id_TipoJust').val(),
            medico: b,
            trabajador: globalTrabajadorId,
            incidencia: globalIncidenciaId,
        };

        $.ajax({
            url: "/sarh/asignarjustificacion",
            data: formData,
            method: "POST",
            async: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            mode: 'same-origin',
            success: function (data) {
                if (data) {
                    if (data.t) {
                        //Si se registra exitosamnte
                        Swal.fire({
                            text: data.name,
                            icon: 'success',
                        });
                        $('#modalCrearJustificante').modal('hide');
                        modificarTabla();
                    } else {
                        //Si no
                        Swal.fire({
                            text: data.name,
                            icon: 'error',
                        });
                    }
                }
            },
            error: function (error) {
                Swal.fire({
                    text: "Algo salió mal, por favor intenta más tarde.",
                    icon: 'error',
                })
            }
        });
    } else {
        Swal.fire({
            text: "Todos los campos son necesarios",
            icon: 'error',
        })
    }
});

function validateFormJustificaion() {
    let id_FechaJust = jQuery('#id_FechaJust').val();
    let id_TipoJust = jQuery('#id_TipoJust').val();
    var validate = true;
    if (id_FechaJust === "") {
        validate = false;
    }
    if (id_TipoJust === "") {
        validate = false;
    }
    return validate;
}
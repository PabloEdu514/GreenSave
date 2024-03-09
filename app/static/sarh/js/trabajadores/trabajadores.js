$(document).ready(function() {
    getLicencias();
    getJustificantes();
    getBeneficiarios();
    getpotenciador();



});




//Método para editar alguna licencia o comisión
$('#eliminarLicencia').on('click', function(e) {
    e.preventDefault();
    let formData = {
        id: jQuery('#id_eliminar_licencia_comision').val(),
    };

    $.ajax({
        url: "/sarh/eliminarlicencia",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data) {
                $('#modaleliminarlicencia').modal('hide');
                getLicencias()

                Swal.fire({
                        text: data.name,
                        icon: 'success',
                        confirmButtonText: 'Cool'
                })


            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });
});


//Método para editar alguna licencia o comisión
$('#editLicencia').on('click', function(e) {
    e.preventDefault();
    if (validateEditarFormLicencia()) {

        let formData = {
            tipo: jQuery('#id_tipo_editar').val(),
            inicia: jQuery('#id_inicia_editar').val(),
            termina: jQuery('#id_termina_editar').val(),
            id: jQuery('#id_lic_editar').val(),
        };

        $.ajax({
            url: "/sarh/editarlicencia",
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
                    getLicencias()
                }
            },
            error: function(error) {
                Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
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

//Método para get_beneficiarios
function getBeneficiarios() {
    let formData = {
        pk: jQuery('#id_trabajador').val(),
    };

    $("#trBeneficiarios").val("").change();

    $.ajax({
        url: "/sarh/get_beneficiarios",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data) {
                /* Primero hacemos un reset de todos los elementos que estaban dentro del select */
                const nodeToReset = document.getElementById("trBeneficiarios");
                nodeToReset.innerHTML = '';

                data.forEach(element => {
                    var rowStructure = `
                    <tr>
                       <td> ` + element.appaterno + ` </td>
                       <td> ` + element.apmaterno + ` </td>
                       <td> ` + element.nombres + ` </td>
                       <td> ` + element.parentesco + ` </td>
                       <td> ` + element.porcentaje + ` </td>
                       <td> 
                          <button type="button" class="btn btn-primary" onclick="getrecorbeneficiario(` + element.id + ` )" data-bs-toggle="modal" data-bs-target="#editarbeneficiario"> 
                          <i class="fas fa-edit fa-sm"></i>
                          </button>
                          <button button type="button" class="btn btn-danger" onclick="eliminarbeneficiario(` + element.id + ` )" data-bs-toggle="modal" data-bs-target="#eliminarbeneficiario"> 
                          <i class="fas fa-trash fa-sm"></i>
                          </button>
                       </td>
                    </tr>
                    `;
                    var dragged = new DOMParser().parseFromString(rowStructure, 'text/xml');
                    var rootNode = document.getElementById("trBeneficiarios");
                    rootNode.insertAdjacentHTML('beforeend', rowStructure);
                });
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });
    if (!$.fn.DataTable.isDataTable('#tablaBeneficiarios')) {
        $("#tablaBeneficiarios").DataTable({
            "responsive": true,
            "lengthChange": false,
            "autoWidth": false,
            "buttons": ["copy", "csv", "excel", "pdf", "print"],
            "dom": 'Bfrtip',
            "language": {
                url: '//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json'
            },
            "ordering": true,
        });
    }
}

//Método para guardar alguna licencia o comisión
$('#saveLicencia').on('click', function(e) {
    e.preventDefault();
    if (validateFormLicencia()) {

        let formData = {
            tipo: jQuery('#id_tipo').val(),
            inicia: jQuery('#id_inicia').val(),
            termina: jQuery('#id_termina').val(),
            trabajador: jQuery('#id_trabajador').val(),
        };

        console.log(formData)

        $.ajax({
            url: "/sarh/asignarlicencia",
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
                    getLicencias()
                }
            },
            error: function(error) {
                Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
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

function validateEditarFormLicencia() {

    let id_tipo = jQuery('#id_tipo_editar').val();
    let id_inicia = jQuery('#id_inicia_editar').val();
    let id_termina = jQuery('#id_termina_editar').val();
    let id_ = jQuery('#id_lic_editar').val();

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
    if (id_ === "") {
        validate = false;
    }
    return validate;
}

function validateEditarFormJustificacion() {

    let id_fecha = jQuery('#id_fecha_editar_just').val();
    let id_tipo = jQuery('#id_tipo_editar_just').val();
    let id_medico = jQuery('#id_medico_editar_just').val();
    let id_ = jQuery('#id_just_editar').val();

    var validate = true;

    if (id_fecha === "") {
        validate = false;
    }
    if (id_tipo === "") {
        validate = false;
    }
    if (id_medico === "") {
        validate = false;
    }
    if (id_ === "") {
        validate = false;
    }

    console.log(validate)
    return validate;
}

function validateFormLicencia() {
    let id_tipo = jQuery('#id_tipo').val();
    let id_inicia = jQuery('#id_inicia').val();
    let id_termina = jQuery('#id_termina').val();
    let id_trabajador = jQuery('#id_trabajador').val();
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
    return validate;
}

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

function getLicencias() {
    id = document.getElementById("trabajador").value
    var tableToDestroy = $('#tablaLicencias').DataTable();
    tableToDestroy.destroy();
    $("#trLicencias").html("");
    $.ajax({
        url: "/sarh/trabajador/" + id + "/licencias",
        type: "get",
        dataType: "json",
        async: false,
        success: function(data) {

            if (data) {
                data.forEach(element => {
                    var rowStructure = `
                    <tr>
                       <td> ` + element.tipo + ` </td>
                       <td> ` + element.inicia + ` </td>
                       <td> ` + element.termina + ` </td>
                       <td> 
                          <button type="button" class="btn btn-primary" onclick="getRecordlicencia(` + element.id + ` )" data-bs-toggle="modal" data-bs-target="#modalEditar" > 
                          <i class="fas fa-edit fa-sm"></i>
                          </button>
                          <button button type="button" class="btn btn-danger" onclick="getRecortoDeleteLic(` + element.id + ` )" data-bs-toggle="modal" data-bs-target="#modaleliminarlicencia" > 
                          <i class="fas fa-trash fa-sm"></i>
                          </button>
                       </td>
                    </tr>
                    `;
                    var dragged = new DOMParser().parseFromString(rowStructure, 'text/xml');
                    var rootNode = document.getElementById("trLicencias");
                    rootNode.insertAdjacentHTML('beforeend', rowStructure);
                });
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });
    if (!$.fn.DataTable.isDataTable('#tablaLicencias')) {
        $("#tablaLicencias").DataTable({
            "responsive": true,
            "lengthChange": false,
            "autoWidth": false,
            "buttons": ["copy", "csv", "excel", "pdf", "print"],
            "dom": 'Bfrtip',
            "language": {
                url: '//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json'
            },
            "ordering": false,
        });
    } // if ! isDataTable
}


function getRecortoDeleteLic(id) {

    $("#id_eliminar_licencia_comision").val(id).change();

}

function getRecordlicencia(id) {

    let formData = {
        id: id,
    };

    $.ajax({
        url: "/sarh/getrecordlicencia",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data) {
                $("#id_tipo_editar").val(data.tipo).change();
                $("#id_inicia_editar").val(formatDate(data.inicia)).change();
                $("#id_termina_editar").val(formatDate(data.termina)).change();
                $("#id_lic_editar").val(data.id).change();
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });

}

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + (d.getDate() + 1),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}


function getRecordJust(id) {

    let formData = {
        id: id,
    };

    $.ajax({
        url: "/sarh/getrecordjust",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data) {

                $("#id_fecha_editar_just").val(formatDate(data.fecha)).change();
                $("#id_tipo_editar_just").val(data.tipo).change();
                $("#id_medico_editar_just").val(data.medico).change();
                $("#id_just_editar").val(id).change();

                if (data.medico == 'true') {
                    $("#id_medico_editar_just").val("true").change();
                } else {
                    $("#id_medico_editar_just").val("false").change();
                }
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });

}

function getJustificantes() {
    id = document.getElementById("trabajador").value
    var tableToDestroy = $('#tablaJustificantes').DataTable();
    tableToDestroy.destroy();
    $("#trJustificantes").html("");
    $.ajax({
        url: "/sarh/trabajador/" + id + "/perfil_justificantes",
        type: "get",
        dataType: "json",
        async: false,
        success: function(data) {
            if (data) {
                data.forEach(element => {
                    var rowStructure = `
                    <tr>
                       <td> ` + element.tipo + ` </td>
                       <td> ` + element.fecha + ` </td>
                       <td> ` + element.medico + ` </td>
                       <td> 
                          <button type="button" class="btn btn-primary" onclick="getRecordJust(` + element.id + ` )" data-bs-toggle="modal" data-bs-target="#modalEditarJust" > 
                          <i class="fas fa-edit fa-sm"></i>
                          </button>
                          <button button onclick="eliminarjusti(` + element.id + ` )" type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#btnEliminarJustificantes" >
                           <i class="fas fa-trash fa-sm"></i>
                          </button>
                       </td>
                       
                    </tr>
                    `;
                    var dragged = new DOMParser().parseFromString(rowStructure, 'text/xml');
                    var rootNode = document.getElementById("trJustificantes");
                    rootNode.insertAdjacentHTML('beforeend', rowStructure);
                });
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });
    if (!$.fn.DataTable.isDataTable('#tablaJustificantes')) {
        $("#tablaJustificantes").DataTable({
            "responsive": true,
            "lengthChange": false,
            "autoWidth": false,
            "buttons": ["copy", "csv", "excel", "pdf", "print"],
            "dom": 'Bfrtip',
            "language": {
                url: '//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json'
            },
            "ordering": false,
        });
    } // if ! isDataTable
}

//obtener Potenciador
function getpotenciador() {
    let formData = {
        trabajador: jQuery('#trabajadorpotenciador').val(),
    };
    $("#getpotenciador").html("");
    $.ajax({
        url: "/sarh/getpotenciador",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data.validate == true) {
                var rowStructure = `
                       <p> Suma asegurada: ` + data.suma_asegurada + ` </p>
                        <p> Potenciación: ` + data.potenciacion + ` </p>                  
                    `;
                var dragged = new DOMParser().parseFromString(rowStructure, 'text/xml');
                var rootNode = document.getElementById("getpotenciador");
                rootNode.insertAdjacentHTML('beforeend', rowStructure);
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });
}
//agregar potenciador
$('#agregarpotenciadorbtn').on('click', function(e) {
    e.preventDefault();
    console.log("hello")
    let formData = {
        trabajador: jQuery('#trabajadorpotenciador').val(),
        potenciador: jQuery('#potenciadoragregar').val()
    };
    $.ajax({
        url: "/sarh/agregarpotenciador",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data) {
                console.log(data.mensaje)
                getpotenciador()
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });
});


//cambiar Potenciador
$('#editarpotenciador').on('click', function(e) {
    e.preventDefault();
    console.log("hello")
    let formData = {
        trabajador: jQuery('#trabajadorpotenciador').val(),
        potenciador: jQuery('#potenciadoreditar').val()
    };
    $.ajax({
        url: "/sarh/editarpotenciador",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data) {
                console.log(data.mensaje)
                getpotenciador()
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });
});


//Método para guardar alguna justificacion
$('#saveJustificante').on('click', function(e) {
    e.preventDefault();
    if (validateFormJustificaion()) {
        var b = new Boolean(false);
        if (jQuery('#id_MedicoJust').val() == "true")
            b = true
        let formData = {
            fecha: jQuery('#id_FechaJust').val(),
            tipo: jQuery('#id_TipoJust').val(),
            medico: b,
            trabajador: jQuery('#id_trabajador').val(),
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
            success: function(data) {
                if (data) {
                    Swal.fire({
                        text: data.name,
                        icon: 'success',
                        confirmButtonText: 'Cool'
                });
                    getJustificantes();
                }
            },
            error: function(error) {
                Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
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

$('#editJustificacion').on('click', function(e) {
    e.preventDefault();

    if (jQuery('#id_medico_editar_just').val() == "true") {
        b = true
    } else {
        b = false
    }

    let formData = {
        fecha: jQuery('#id_fecha_editar_just').val(),
        tipo: jQuery('#id_tipo_editar_just').val(),
        medico: b,
        id: jQuery('#id_just_editar').val(),
    };

    $.ajax({
        url: "/sarh/editarjustificacion",
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
                getJustificantes()
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });

});

function eliminarjusti(id) {
    $("#eliminar_justificacion").val(id).change();
}

//Método para eliminarJustificacion
$('#eliminarJust').on('click', function(e) {

    e.preventDefault();

    let formData = {
        id: jQuery('#eliminar_justificacion').val()
    };

    $.ajax({
        url: "/sarh/eliminarjusti",
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
                getJustificantes()
            }
        },
        error: function(error) {
            Swal.fire({
                        text: "Algo salió mal, por favor intenta más tarde",
                        icon: 'error',
                })
        }
    });
});



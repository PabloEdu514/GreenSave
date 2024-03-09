$(document).ready(function () {
    $('#ocultarPeriodoVacacional').hide();
    $("#justificantesGenerales").DataTable({
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
    $("#diasOficiales").DataTable({
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
    $("#periodos").DataTable({
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
    $('#id_departamento_').multiselect({
        buttonWidth: '100%',
        includeSelectAllOption: true,
        nonSelectedText: 'Selecciona los departamentos...',
        nSelectedText: ' - departamentos seleccionados.',
        allSelectedText: 'Todos ...'

    });
    $('#id_departamento').select2({
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('Selecciona los departamentos...'),
        closeOnSelect: false,
        tags: true
    });
    $('#nombre_ocultardoFinal').change(function (e) {
        if ($('#nombre_ocultardoFinal').val() == '') {
            $('#ocultarPeriodoVacacional').hide();
            $('#fin_ocultardoFinal').val('');
        }else if ($('#nombre_ocultardoFinal').val() == 'Dia oficial no laboral') {
            $('#ocultarPeriodoVacacional').hide();
            $('#fin_ocultardoFinal').val('');
        }else{
            $('#ocultarPeriodoVacacional').show();
        }
    });
});

function getDONL(id) {

    let formData = {
        id: id,
    };

    $.ajax({
        url: "/sarh/getDONL",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
            if (data) {
                $("#nombre_editar").val(data.nombre).change();
                $("#inicio_editar").val(data.inicio).change();
                $("#fin_editar").val(data.fin).change();
                $("#idDiaEditar").val(data.id).change();
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

$('#saveDONL').on('click', function (e) {
    e.preventDefault();
    let formData = {
        id: jQuery('#idDiaEditar').val(),
        inicio: jQuery('#inicio_editar').val(),
        fin: jQuery('#fin_editar').val(),
        nombre: jQuery('#nombre_editar').val()
    };
    console.log(formData)
    $.ajax({
        url: "/sarh/editDONL",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
            if (data) {
                Swal.fire({
                    text: data.name,
                    icon: 'success',
                    confirmButtonText: 'Cool'
                })
                //getHistorial()
                // location.reload()
                setTimeout(function(){
                    window.location.href = '/sarh/calendario/DONLEditExito/'
                }, 2000);
            }
        },
        error: function (error) {
            Swal.fire({
                text: "Algo salió mal, por favor intenta más tarde",
                icon: 'error',
                confirmButtonText: 'Cool'
            })
        }
    });
});

function getJG(id) {

    let formData = {
        id: id,
    };

    $.ajax({
        url: "/sarh/getJG",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
            if (data) {
                $("#idDiaEditarJG").val(data.id).change();
                $("#nombre_editarJG").val(data.nombre).change();
                $("#horaInicio_editarJG").val(data.horaInicio).change();
                $("#horaFin_editarJG").val(data.horaFin).change();
                $("#departamento_editarJG").val(data.departamento).change();
                $("#dia_editarJG").val(data.dia).change();
                if (data.base.toString() == 'true') {
                    $("#base_editarJG").prop("checked", true);
                } else {
                    $("#base_editarJG").prop("checked", false);
                }
                if (data.honorario.toString() == 'true') {
                    $("#honorario_editarJG").prop("checked", true);
                } else {
                    $("#honorario_editarJG").prop("checked", false);
                }
                if (data.asimilado.toString() == 'true') {
                    $("#asimilado_editarJG").prop("checked", true);
                } else {
                    $("#asimilado_editarJG").prop("checked", false);
                }
                if (data.administrativo.toString() == 'true') {
                    $("#administrativo_editarJG").prop("checked", true);
                } else {
                    $("#administrativo_editarJG").prop("checked", false);
                }
                if (data.docente.toString() == 'true') {
                    $("#docente_editarJG").prop("checked", true);
                } else {
                    $("#docente_editarJG").prop("checked", false);
                }
                $("#genero_editarJG").val(data.genero).change();
            }
        },
        error: function (error) {
            console.log(error);
        }
    });

}

$('#saveJG').on('click', function (e) {
    e.preventDefault();
    let formData = {
        id: jQuery('#idDiaEditarJG').val(),
        nombre: jQuery('#nombre_editarJG').val(),
        dia: jQuery('#dia_editarJG').val(),
        horaInicio: jQuery('#horaInicio_editarJG').val(),
        horaFin: jQuery('#horaFin_editarJG').val(),
        // base: jQuery('#base_editarJG').value(),
        // honorario: jQuery('#honorario_editarJG').val(),
        // asimilado: jQuery('#asimilado_editarJG').val(),
        // administrativo: jQuery('#administrativo_editarJG').val(),
        // docente: jQuery('#docente_editarJG').val(),
        genero: jQuery('#genero_editarJG').val(),
        departamento: jQuery('#departamento_editarJG').val()
    };
    if ($('#base_editarJG').prop('checked')) {
        formData.base = 'on'
    }
    if ($('#honorario_editarJG').prop('checked')) {
        formData.honorario = 'on'
    }
    if ($('#asimilado_editarJG').prop('checked')) {
        formData.asimilado = 'on'
    }
    if ($('#administrativo_editarJG').prop('checked')) {
        formData.administrativo = 'on'
    }
    if ($('#docente_editarJG').prop('checked')) {
        formData.docente = 'on'
    }
    console.log(formData)
    $.ajax({
        url: "/sarh/editJG",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
            if (data) {
                Swal.fire({
                    text: data.name,
                    icon: 'success',
                    confirmButtonText: 'Cool'
                })
                //getHistorial()
                // location.reload()
                setTimeout(function(){
                    window.location.href = '/sarh/calendario/JustEditExito/'
                }, 2000);
            }
        },
        error: function (error) {
            Swal.fire({
                text: "Algo salió mal, por favor intenta más tarde",
                icon: 'error',
                confirmButtonText: 'Cool'
            })
        }
    });
});

function getPer(id) {

    let formData = {
        id: id,
    };

    $.ajax({
        url: "/sarh/getPE",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
            if (data) {
                $("#idEditarPer").val(data.id).change();
                $("#periodoh_editarPE").val(data.periodoh).change();
                $("#fecha_inicia_editarPE").val(data.fecha_inicia).change();
                $("#fecha_termina_editarPE").val(data.fecha_termina).change();
                if (data.activo.toString() == 'true') {
                    $("#activo_editarPE").prop("checked", true);
                } else {
                    $("#activo_editarPE").prop("checked", false);
                }
            }
        },
        error: function (error) {
            console.log(error);
        }
    });

}

$('#savePE').on('click', function (e) {
    e.preventDefault();
    let formData = {
        id: jQuery('#idEditarPer').val(),
        periodoh: jQuery('#periodoh_editarPE').val(),
        fecha_inicia: jQuery('#fecha_inicia_editarPE').val(),
        fecha_termina: jQuery('#fecha_termina_editarPE').val(),
        activo:''
    };
    if ($('#activo_editarPE').prop('checked')) {
        formData.activo = true
    }else{
        formData.activo = false
    }
    
    $.ajax({
        url: "/sarh/editPE",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
            if (data) {
                if(data.name != 'error'){
                    Swal.fire({
                        text: data.name,
                        icon: 'success',
                        confirmButtonText: 'Cool'
                    })
                    setTimeout(function(){
                        window.location.href = '/sarh/calendario/PerEditExito/'
                    }, 2000);
                }else{
                    Swal.fire({
                        text: "Algo salió mal, por favor revisa los datos",
                        icon: 'error',
                        confirmButtonText: 'Cool'
                    })
                }
                //getHistorial()
                // location.reload()
                
            }
        },
        error: function (error) {
            Swal.fire({
                text: "Algo salió mal, por favor intenta más tarde",
                icon: 'error',
                confirmButtonText: 'Cool'
            })
            setTimeout(function(){
                window.location.href = '/sarh/calendario/PerEditError/'
            }, 2000);
        }
    });
});

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

        $.ajax({
            url: "/asignarlicencia",
            data: formData,
            method: "POST",
            async: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            mode: 'same-origin',
            success: function(data) {
                if (data) {
                $('#alertaexito').removeAttr('hidden');
                    $('#alertamal').prop('hidden', true);
                    document.getElementById("formLic").reset();
                }
            },
            error: function(error) {
                $('#alertamal').removeAttr('hidden');
        $('#alertaexito').prop('hidden', true);
            }
        });
    } else {
             $('#alertamal').removeAttr('hidden');
        $('#alertaexito').prop('hidden', true);
    }
});


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

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + (d.getDate()+1),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}


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
            url: "/asignarjustificacion",
            data: formData,
            method: "POST",
            async: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            mode: 'same-origin',
            success: function(data) {
                if (data) {
                    $('#alertaexito2').removeAttr('hidden');
                    $('#alertamal2').prop('hidden', true);
                                        document.getElementById("formLic").reset();
                }
            },
            error: function(error) {
                $('#alertamal2').removeAttr('hidden');
                $('#alertaexito2').prop('hidden', true);
            }
        });
    } else {
        $('#alertamal2').removeAttr('hidden');
        $('#alertaexito2').prop('hidden', true);
    }
});

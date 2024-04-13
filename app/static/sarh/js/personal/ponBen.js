$(document).ready(function () {
    getBeneficiarios();
    getpotenciador();
});

//Método para get_beneficiarios
function getBeneficiarios() {
    let formData = {
        pk: jQuery('#id_trabajador').val(),
    };
    // console.log(document.querySelector('[name=csrfmiddlewaretoken]').value)
    $("#trBeneficiarios").val("").change();
    $.ajax({
        url: "/sarh/getBeneficiarios",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
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
        error: function (error) {
            Swal.fire({
                text: "Algo salió mal, por favor intenta más tarde",
                icon: 'error',
            })
            // console.log("error");
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

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + (d.getDate() + 1),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}

//obtener Potenciador
function getpotenciador() {
    let formData = {
        trabajador: jQuery('#trabajadorpotenciador').val(),
    };
    $("#getpotenciador").html("");
    $.ajax({
        url: "/sarh/get_potenciador",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
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
        error: function (error) {
            Swal.fire({
                text: "Algo salió mal, por favor intenta más tarde",
                icon: 'error',
            })
        }
    });
}

//agregar potenciador
$('#agregarpotenciadorbtn').on('click', function (e) {
    e.preventDefault();
    console.log("hello")
    let formData = {
        trabajador: jQuery('#trabajadorpotenciador').val(),
        potenciador: jQuery('#potenciadoragregar').val()
    };
    $.ajax({
        url: "/sarh/agregar_potenciador",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
            if (data) {
                console.log(data.mensaje)
                getpotenciador()
            }
        },
        error: function (error) {
            Swal.fire({
                text: "Algo salió mal, por favor intenta más tarde",
                icon: 'error',
            })
        }
    });
});

//cambiar Potenciador
$('#editarpotenciador').on('click', function (e) {
    e.preventDefault();
    console.log("hello")
    let formData = {
        trabajador: jQuery('#trabajadorpotenciador').val(),
        potenciador: jQuery('#potenciadoreditar').val()
    };
    $.ajax({
        url: "/sarh/editar_potenciador",
        data: formData,
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
            if (data) {
                console.log(data.mensaje)
                getpotenciador()
            }
        },
        error: function (error) {
            Swal.fire({
                text: "Algo salió mal, por favor intenta más tarde",
                icon: 'error',
            })
        }
    });
});

function eliminarbeneficiario(id) {
    $("#registroBeneficiario").val(id).change();
}

function getrecorbeneficiario(id) {
    $.ajax({
        url: "/sarh/getrecordBeneficiario",
        data: {
            'pk': id
        },
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function (data) {
            if (data) {

                if (data.validate == true) {
                    $("#nombresbeneficiarioedit").val(data.nombres).change();
                    $("#appaternobeneficiarioedit").val(data.appaterno).change();
                    $("#apmaternobeneficiarioedit").val(data.apmaterno).change();
                    $("#parentescobeneficiarioedit").val(data.parentesco).change();
                    $("#porcentajebeneficiarioedit").val(data.porcentaje).change();
                    $("#pkedittbeneficiario").val(data.pk).change();
                }
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

//updatebeneficiario
$('#updateBeneficiario').on('click', function (e) {
    e.preventDefault();
    if (validateFormBeneficiarioedit) {

        let formData = {
            trabajadorbeneficiario: jQuery('#trabajadorbeneficiario').val(),
            porcentajebeneficiario: jQuery('#porcentajebeneficiarioedit').val(),
            parentescobeneficiario: jQuery('#parentescobeneficiarioedit').val(),
            apmaternobeneficiario: jQuery('#apmaternobeneficiarioedit').val(),
            appaternobeneficiario: jQuery('#appaternobeneficiarioedit').val(),
            nombresbeneficiario: jQuery('#nombresbeneficiarioedit').val(),
            pkbeneficiario: jQuery('#pkedittbeneficiario').val(),
        };

        console.log(formData)

        $.ajax({
            url: "/sarh/editBeneficiario",
            data: formData,
            method: "POST",
            async: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            mode: 'same-origin',
            success: function (data) {
                if (data) {
                    getBeneficiarios();
                    console.log(data)
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    } else {
        Swal.fire({
            text: "Todos los campos son necesarios",
            icon: 'error',
        })
    }
});

function validateFormBeneficiarioedit() {
    let trabajadorbeneficiario = jQuery('#trabajadorbeneficiarioedit').val();
    let porcentajebeneficiario = jQuery('#porcentajebeneficiarioedit').val();
    let parentescobeneficiario = jQuery('#parentescobeneficiarioedit').val();
    let apmaternobeneficiario = jQuery('#apmaternobeneficiarioedit').val();
    let appaternobeneficiario = jQuery('#appaternobeneficiarioedit').val();
    let nombresbeneficiario = jQuery('#nombresbeneficiarioedit').val();

    var validate = true;
    if (trabajadorbeneficiario === "") {
        validate = false;
    }
    if (porcentajebeneficiario === "" || porcentajebeneficiario <= 0) {
        validate = false;
    }
    if (parentescobeneficiario === "") {
        validate = false;
    }
    if (apmaternobeneficiario === "") {
        validate = false;
    }
    if (appaternobeneficiario === "") {
        validate = false;
    }
    if (nombresbeneficiario === "") {
        validate = false;
    }
    return validate;
}

$('#eliminarBeneficiario').on('click', function (e) {
    e.preventDefault();
    if (validateFormBeneficiario) {
        let formData = {
            pk: jQuery('#registroBeneficiario').val(),
        };
        $.ajax({
            url: "/sarh/deleteBeneficiario",
            data: formData,
            method: "POST",
            async: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            mode: 'same-origin',
            success: function (data) {
                if (data) {
                    console.log(data)
                    getBeneficiarios();
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    } else {
        Swal.fire({
            text: "Todos los campos son necesarios",
            icon: 'error',
        })
    }
});

//Método para guardar alguna licencia o comisión
$('#saveBeneficiario').on('click', function (e) {
    e.preventDefault();
    console.log("formulario para guardar un beneficiario nuevo")
    if (validateFormBeneficiario) {
        let formData = {
            trabajadorbeneficiario: jQuery('#trabajadorbeneficiario').val(),
            porcentajebeneficiario: jQuery('#porcentajebeneficiario').val(),
            parentescobeneficiario: jQuery('#parentescobeneficiario').val(),
            apmaternobeneficiario: jQuery('#apmaternobeneficiario').val(),
            appaternobeneficiario: jQuery('#appaternobeneficiario').val(),
            nombresbeneficiario: jQuery('#nombresbeneficiario').val(),
            nombresbeneficiario: jQuery('#nombresbeneficiario').val(),
        };

        $.ajax({
            url: "/sarh/addBeneficiario",
            data: formData,
            method: "POST",
            async: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            mode: 'same-origin',
            success: function (data) {
                if (data) {
                    console.log(data)
                    getBeneficiarios();
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    } else {
        Swal.fire({
            text: "Todos los campos son necesarios",
            icon: 'error',
        })
    }
});

function validateFormBeneficiario() {
    let trabajadorbeneficiario = jQuery('#trabajadorbeneficiario').val();
    let porcentajebeneficiario = jQuery('#porcentajebeneficiario').val();
    let parentescobeneficiario = jQuery('#parentescobeneficiario').val();
    let apmaternobeneficiario = jQuery('#apmaternobeneficiario').val();
    let appaternobeneficiario = jQuery('#appaternobeneficiario').val();
    let nombresbeneficiario = jQuery('#nombresbeneficiario').val();

    var validate = true;
    if (trabajadorbeneficiario === "") {
        validate = false;
    }
    if (porcentajebeneficiario === "" || porcentajebeneficiario <= 0) {
        validate = false;
    }
    if (parentescobeneficiario === "") {
        validate = false;
    }
    if (apmaternobeneficiario === "") {
        validate = false;
    }
    if (appaternobeneficiario === "") {
        validate = false;
    }
    if (nombresbeneficiario === "") {
        validate = false;
    }
    return validate;
}


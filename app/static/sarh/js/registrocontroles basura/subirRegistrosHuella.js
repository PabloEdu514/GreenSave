var parsed, regBien, regMal;
$(document).ready(function () {
    document.getElementById('pantallas-reg').style.display = 'none';

    //Extract trabajadores
    var data_json = document.querySelector('#jsonData').getAttribute('data-json');
    const validJson = data_json.replaceAll(`'`, `"`);
    parsed = JSON.parse(validJson);
    //llenarTabla();
});

function editReg(ren) {
    var table = $('#tablaDeRegistros').DataTable();
    var tableData = table.rows(ren).data().toArray();
    var tableDataRow = tableData[0]

    document.getElementById("id_trabajador_editar_reg").value = tableDataRow[1];
    document.getElementById("id_fecha_editar_reg").value = tableDataRow[3];
    document.getElementById("id_reg_editar").value = ren;
    document.getElementById("id_hora_editar_reg").value = tableDataRow[4];
}

$('#editRegistro').on('click', function (e) {
    //alert(document.getElementById("id_reg_editar").value)

    var table = $('#tablaDeRegistros').dataTable();
    var temp = []
    temp[0] = parseInt(document.getElementById("id_reg_editar").value) + 1;
    temp[1] = document.getElementById("id_trabajador_editar_reg").value;

    var nombre;
    try {
        var result = parsed.filter(obj => {
            return obj.id === parseInt(temp[1])
        })
        nombre = result[0].nombre;
    } catch (error) {
        nombre = 'No encontrado'
    }

    temp[2] = nombre;
    temp[3] = document.getElementById("id_fecha_editar_reg").value;
    temp[4] = document.getElementById("id_hora_editar_reg").value;
    temp[5] = ` <button type="button" class="btn btn-primary" onclick="editReg(` + document.getElementById("id_reg_editar").value + `)" data-bs-toggle="modal" data-bs-target="#modalEditarRegistro" > 
    <i class="fas fa-edit fa-sm"></i>
    </button>`
    table.fnUpdate(temp, document.getElementById("id_reg_editar").value, undefined, false);
    $('#modalEditarRegistro').modal('hide');
});

$('#saveRegistros').on('click', function (e) {
    e.preventDefault();

    try {
        var arreglo = []
        var myTab = document.getElementById('tablaDeRegistros');

        //Obtenemos dataTable
        var table = $('#tablaDeRegistros').DataTable();

        //Recorrer de renglon por renglon
        for (i = 0; i < table.rows().data().length; i++) {
            //Extrae el renglon i del dataTable (lo devuelve en arreglo)
            var tableData = table.rows(i).data().toArray();
            var tableDataRow = tableData[0]

            var iTrabajador = tableDataRow[1]
            if (!valTrabajador(iTrabajador)) {
                throw 'Error: En el renglon ' + i + 'con columna trabajador'
            }
            var iFecha = tableDataRow[3]
            if (!valFecha(iFecha)) {
                throw 'Error: En el renglon ' + i + 'con columna fecha'
            }
            var iHora = tableDataRow[4]
            if (!valHora(iHora)) {
                throw 'Error: En el renglon ' + i + 'con columna hora'
            }

            var registro = {
                trabajador: iTrabajador,
                fecha: iFecha,
                hora: iHora
            }

            arreglo.push(registro)
        }

        let formData = {
            array: JSON.stringify(arreglo),
        };
        $.ajax({
            url: "/postRegistro",
            data: formData,
            method: "POST",
            async: false,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            mode: 'same-origin',
            success: function (data) {
                regBien = data.regBien
                regMal = data.regMal
                var tableToDestroy = $('#tablaDeRegistros').DataTable();
                tableToDestroy.clear().draw;
                //
                document.getElementById('pantallas-reg').style.display = 'block';
                document.getElementById('table').style.display = 'none';
                document.getElementById('mensajeError').style.display = 'none';
                displayRegs();
            },
            error: function (error) {
                alert("ERROR: Algo salio mal al subir los registros.")
            }
        });
    } catch (error) {
        alert(error)
    }
});

function displayRegs() {
    var tableToDestroy = $('#tablaRegSubidos').DataTable();
    tableToDestroy.destroy();
    $("#tableBodySubidos").html("");

    var i = 1;
    regBien.forEach(element => {
        var nombre;

        try {
            var result = parsed.filter(obj => {
                return obj.id === parseInt(element.id)
            })
            nombre = result[0].nombre;
        } catch (error) {
            nombre = 'No encontrado'
        }
        var rowStructure = `
            <tr>
                <td>` + (i++) + `</td>
                <td>` + element.id + `</td>
                <td>` + nombre + `</td>
                <td>` + element.fecha + `</td>
                <td>` + element.hora + `</td>
            </tr>
        `;
        var dragged = new DOMParser().parseFromString(rowStructure, 'text/xml');
        var rootNode = document.getElementById("tableBodySubidos");
        rootNode.insertAdjacentHTML('beforeend', rowStructure);
    });

    if (!$.fn.DataTable.isDataTable('#tablaRegSubidos')) {
        $("#tablaRegSubidos").DataTable({
            "responsive": true,
            "lengthChange": false,
            "autoWidth": false,
            "buttons": ["copy", "csv", "excel", "pdf", "print"],
            "dom": 'Bfrtip',
            "language": {
                url: '//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json'
            },
            "ordering": false,
            "pageLength": 25,
            "contentEditable": true,
        });
    }

    //Otra tabla
    var tableToDestroy = $('#tablaRegConflicto').DataTable();
    tableToDestroy.destroy();
    $("#tableBodyConflicto").html("");
    var i = 1;

    regMal.forEach(element => {
        var nombre;

        try {
            var result = parsed.filter(obj => {
                return obj.id === parseInt(element.id)
            })
            nombre = result[0].nombre;
        } catch (error) {
            nombre = 'No encontrado'
        }

        var rowStructure = `
            <tr>
                <td>` + (i++) + `</td>
                <td>` + element.id + `</td>
                <td>` + nombre + `</td>
                <td>` + element.fecha + `</td>
                <td>` + element.hora + `</td>
            </tr>
        `;
        var dragged = new DOMParser().parseFromString(rowStructure, 'text/xml');
        var rootNode = document.getElementById("tableBodyConflicto");
        rootNode.insertAdjacentHTML('beforeend', rowStructure);
    });

    if (!$.fn.DataTable.isDataTable('#tablaRegConflicto')) {
        $("#tablaRegConflicto").DataTable({
            "responsive": true,
            "lengthChange": false,
            "autoWidth": false,
            "buttons": ["copy", "csv", "excel", "pdf", "print"],
            "dom": 'Bfrtip',
            "language": {
                url: '//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json'
            },
            "ordering": false,
            "pageLength": 25,
            "contentEditable": true,
        });
    }
}

function isTrabajador(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 47 && charCode < 58) {
        return true;
    }
    return false;
}
function valTrabajador(text) {
    const re = /[0-9]{1,4}/;
    const ok = re.exec(text);

    if (text == ok[0]) {
        return true
    } else {
        return false
    }
}
function valFecha(text) {
    const re = /[0-9]{1,4}[-][0-9]{2}[-][0-9]{2}/;
    const ok = re.exec(text);

    if (text == ok[0]) {
        return true
    } else {
        return false
    }
}
function valHora(text) {
    const re = /[0-9]{2}[:][0-9]{2}/;
    const ok = re.exec(text);

    if (text == ok[0]) {
        return true
    } else {
        return false
    }
}
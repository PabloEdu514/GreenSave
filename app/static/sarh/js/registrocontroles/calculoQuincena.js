$(document).ready(function () {
    $(".spinner-border").hide();    
    $(".genera").hide();  
    // $("#id_numero").change(function () { 
    //     let val= $("#id_numero").val();
    //     if (0< val <=24) {
    //         let anio = $("#id_anio").val();
    //         if(anio != ''){
    //             calcfech(val, anio);
    //         }
    //     }
    // });
    $("#id_anio").change(function () { 
        let anio = $("#id_anio").val();
        if (anio != '') {
            let val = $("#id_nombreQuin").val();
            if (0< val <=24 && val != '') {
                calcfech(val, anio);
            }
        }
        
    });

    $(".btnBuscar").click(function () { 
        $('.spinner-border').show();
        $(".genera").show();  
    });

    $('#id_nombreQuin').select2({
        dropdownParent: $('#selecQuincena'),
        width: 'resolve'
     });
    
     $('#id_year').select2({
        dropdownParent: $('#selecIncMes'),
        width: 'resolve'
     });

    $("#id_nombreQuin").change( function() {
        let val= $("#id_nombreQuin").val();
        if (0< val <=24) {
            let anio = $("#id_anio").val();
            if(anio != ''){
                calcfech(val, anio);
            }
        }
    });
    
});

function calcfech(val, anio) {   
    let mes = val/2;
    if(val%2 != 0){
        mes+=0.5;
    }
    mes--;
    let dia = 0;
    if ((val % 2) != 0) {
        dia = 1;
    }
    else{
        dia = 16;
    }
    if (mes == 1) {
        var now = new Date(anio, mes, dia);
        if (dia == 1) { 
            dia+=14
            var termina = new Date(anio, mes, dia) 
            if(mes < 9){
                $("#id_inicioQuincena").val(now.getFullYear()+"-0"+(now.getMonth()+1)+"-0"+now.getDate());
                $("#id_finQuincena").val(termina.getFullYear()+"-0"+(termina.getMonth()+1)+"-"+termina.getDate());
            }
            else{
                $("#id_inicioQuincena").val(now.getFullYear()+"-"+(now.getMonth()+1)+"-0"+now.getDate());
                $("#id_finQuincena").val(termina.getFullYear()+"-"+(termina.getMonth()+1)+"-"+termina.getDate());
            }
        }
        else{
            dia+=12
            mes++
            var termina = new Date(anio, mes, 0)
            if(mes <= 9){
                $("#id_inicioQuincena").val(now.getFullYear()+"-0"+(now.getMonth()+1)+"-"+now.getDate());
                $("#id_finQuincena").val(termina.getFullYear()+"-0"+(termina.getMonth()+1)+"-"+termina.getDate());
            }
            else{
                $("#id_inicioQuincena").val(now.getFullYear()+"-"+(now.getMonth()+1)+"-0"+now.getDate());
                $("#id_finQuincena").val(termina.getFullYear()+"-"+(termina.getMonth()+1)+"-"+termina.getDate());
            }
        }
    }
    else{
        var now = new Date(anio, mes, dia);
        if (dia == 1) { 
            dia+=14
            var termina = new Date(anio, mes, dia);
            if(mes < 9){
                $("#id_inicioQuincena").val(now.getFullYear()+"-0"+(now.getMonth()+1)+"-0"+now.getDate());
                $("#id_finQuincena").val(termina.getFullYear()+"-0"+(termina.getMonth()+1)+"-"+termina.getDate());
            }
            else{
                $("#id_inicioQuincena").val(now.getFullYear()+"-"+(now.getMonth()+1)+"-0"+now.getDate());
                $("#id_finQuincena").val(termina.getFullYear()+"-"+(termina.getMonth()+1)+"-"+termina.getDate());
            }
        }
        else{
            dia+=14
            mes++
            var termina = new Date(anio, mes, 0);
            if(mes <= 9){
                $("#id_inicioQuincena").val(now.getFullYear()+"-0"+(now.getMonth()+1)+"-"+now.getDate());
                $("#id_finQuincena").val(termina.getFullYear()+"-0"+(termina.getMonth()+1)+"-"+termina.getDate());
            }
            else{
                $("#id_inicioQuincena").val(now.getFullYear()+"-"+(now.getMonth()+1)+"-"+now.getDate());
                $("#id_finQuincena").val(termina.getFullYear()+"-"+(termina.getMonth()+1)+"-"+termina.getDate());
            }
        }
    }
}

function getRegXDia(id){
    $.ajax({
        type: "get",
        url: "/sarh/getRegXDia",
        dataType: "json",
        data: {'id':id},
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        success: function (response) { 
            regChec = response.registrosChec
            regLib = response.registrosLib

            registros = ""
            registros += `
            <li> Checador </li>          
            `;
            regChec.map(registro => {
                if(registro.hora != null){
                    registros += `
                            <li> ${registro.hora} </li>
                            `;
                }
                // console.log(registro.hora)
            });
            registros += `
                        <li> ---------- </li>                        
                        <li> Libro </li>
                        `;
            regLib.map(registro => {
                if(registro.reg_ent != null || registro.reg_sal != null){
                    if(registro.reg_ent != null){
                        registros += `
                                <li> ${registro.reg_ent} </li>
                                `;                    
                    }
                    if(registro.reg_sal != null){
                        registros+=`
                                <li> ${registro.reg_sal} </li>
                                `;
                    }
                      
                }
                // console.log(registro.reg_ent)
                // console.log(registro.reg_sal)
            });

            $("#"+id).html(registros);

            // console.log(response)
            // console.log(regChec)
            // console.log(regLib)
            // console.log(regLib)
        },
        error: function(response){
            console.log(response.responseJSON.errors)
        }
    });
}

function descuentoInc(id, renglonTabla){
    console.log(renglonTabla)
    $.ajax({
        url: "/sarh/descuentoIncidencia",
        type: "post",
        dataType : "json",
        data: {'incidencia' :  parseInt(id)},
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        success: data => {
            console.log(data)
        },
        error: error => {
            console.log(error)
        }
    });
    modificarTablaInc(renglonTabla)

}

function setFieldTrab(trabajador, dia, mes, year, tipo) {
    // console.log(year)
    const fieldTrabajador = document.getElementById('id_trabajador')
    const fieldDia = document.getElementById('id_dia')
    const fieldMes = document.getElementById('id_mes')
    const fieldYear = document.getElementById('id_anioInc')
    const fieldTipo = document.getElementById('id_tipo')
    fieldTrabajador.value = trabajador
    fieldDia.value =  dia
    fieldMes.value = mes
    fieldYear.value = year
    fieldTipo.value = tipo
    $.ajax({
        url: "/sarh/getNumOficio",
        type: "post",
        dataType : "json",
        data: {},
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        success: data => {
            console.log(data)
            const inputNumeroOficio = $("#id_numeroOficio").val(parseInt(data.num) + 1);
        },
        error: error => {
            console.log(error)
        }
    });
}

function modificarTablaInc(renglonTabla) {
    console.log('entrando')
    var tablaIncidencias = $('#tablaDeIncidencias').dataTable();
    //1) Valor a meter
    //2) Renglon donde se mete
    //3) Columna donde se mete
    //4) Para no recargar la tabla
    //NOTA: Para editar un renglon completo ver subirRegistrosHuella.js
    tablaIncidencias.fnUpdate('<p style="color: orange;">Descontar</p>', renglonTabla, 6, false);
    codigo = ` 
    <ul class="navbar-nav" onclick="getRegXDia({{incidencia.id}})" title="Ver registros del día">
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
    `
    console.log('Codigo a meter:'+codigo)
    tablaIncidencias.fnUpdate(codigo, renglonTabla, 7, false);
    }
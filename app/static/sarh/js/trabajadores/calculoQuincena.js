$(document).ready(function () {
    $(".spinner-border").hide();    
    $(".genera").hide();  
    let num = document.getElementById('#id_numero');
    $("#id_numero").change(function () { 
        let val= $("#id_numero").val();
        if (0< val <=24) {
            let anio = $("#id_anio").val();
            if(anio != ''){
                calcfech(val, anio);
            }
        }
    });
    $("#id_anio").change(function () { 
        let anio = $("#id_anio").val();
        if (anio != '') {
            let val = $("#id_numero").val();
            if (0< val <=24 && val != '') {
                calcfech(val, anio);
            }
        }
        
    });

    $(".btnBuscar").click(function () { 
        $('.spinner-border').show();
        $(".genera").show();  
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
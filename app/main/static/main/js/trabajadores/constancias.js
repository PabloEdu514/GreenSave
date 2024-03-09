const input = document.getElementById('id_anio');
input.addEventListener('change', anioTexto);

const input2 = document.getElementById('extra_anio');
input2.addEventListener('change', anioTexto);

function anioTexto(e){
    val1 = e.target.value;
    idSor = e.target.id;
    $.ajax({
        url: "/numtext/",
        data: {
            'num': val1
        },
        method: "POST",
        async: false,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        mode: 'same-origin',
        success: function(data) {
            if (data) {
                if (idSor == 'id_anio') {
                    $('#id_anionom').val(data.numero)
                } else {
                    $('#extra_anionom').val(data.numero)
                }
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function cambioForm(accion) {
    $('#formOficios').attr('action', accion);
}
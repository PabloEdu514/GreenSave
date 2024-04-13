let trabajadores = ["Madres", "Justificantes", "Personal", "Calendario", "Registro de asistencia manual", "Registro de asistencia de checador", "Redacción de correo", "Incidencias"];
let respuesta;

$.ajax({
    type: "get",
    url: "/sarh/busqueda",
    dataType: "json",
    success: function (response) {
        response.forEach(element => {
            trabajadores.push(element.nombre)
        });
        respuesta = response;
    }
});
const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("#buscar");
const suggBox = searchWrapper.querySelector(".autocom-box");
inputBox.onkeyup = (e) => {
    let userData = e.target.value; //user enetered data
    let emptyArray = [];
    if (userData) {
        emptyArray = trabajadores.filter((data) => {
            if (data.toLocaleLowerCase().indexOf(userData.toLocaleLowerCase()) != -1) {
                return true;
            } else {
                return false;
            }
        });
        emptyArray = emptyArray.map((data) => {
            switch (data) {
                case "Madres":
                    url = '';
                    respuesta.forEach(element => {
                        if (element.nombre == 'varios') {
                            url = element.urlMadres
                        }
                    });
                    return data = `<a href="${url}"><li class="li-search">${data}</li></a>`
                    break;
                case "Justificantes":
                    url = '';
                    respuesta.forEach(element => {
                        if (element.nombre == 'varios') {
                            url = element.urlJustificantes
                        }
                    });
                    return data = `<a href="${url}"><li class="li-search">${data}</li></a>`
                    break;
                case "Personal":
                    url = '';
                    respuesta.forEach(element => {
                        if (element.nombre == 'varios') {
                            url = element.urlPersonal
                        }
                    });
                    return data = `<a href="${url}"><li class="li-search">${data}</li></a>`
                    break;
                case "Calendario":
                    url = '';
                    respuesta.forEach(element => {
                        if (element.nombre == 'varios') {
                            url = element.urlCalendario
                        }
                    });
                    return data = `<a href="${url}"><li class="li-search">${data}</li></a>`
                    break;
                case "Registro de asistencia manual":
                    url = '';
                    respuesta.forEach(element => {
                        if (element.nombre == 'varios') {
                            url = element.urlRegistro1
                        }
                    });
                    return data = `<a href="${url}"><li class="li-search">${data}</li></a>`
                    break;
                case "Registro de asistencia de checador":
                    url = '';
                    respuesta.forEach(element => {
                        if (element.nombre == 'varios') {
                            url = element.urlRegistro2
                        }
                    });
                    return data = `<a href="${url}"><li class="li-search">${data}</li></a>`
                    break;
                case "Redacción de correo":
                    url = '';
                    respuesta.forEach(element => {
                        if (element.nombre == 'varios') {
                            url = element.urlCorreo
                        }
                    });
                    return data = `<a href="${url}"><li class="li-search">${data}</li></a>`
                    break;
                case "Incidencias":
                    url = '';
                    respuesta.forEach(element => {
                        if (element.nombre == 'varios') {
                            url = element.urlIncidencias
                        }
                    });
                    return data = `<a href="${url}"><li class="li-search">${data}</li></a>`
                    break;

                default:
                    id = 0;
                    url1 = '';
                    url2 = '';
                    url3 = '';
                    respuesta.forEach(element => {
                        if (element.nombre == data) {
                            id = element.id
                            url1 = element.urlTrabajador
                            url2 = element.urlEditar
                            url3 = element.urlHorario
                        }
                    });
                    nombreSolo = data.split(" - ")[0]
                    return data = `<div class="dropdown nav-item"><a href="#" data-bs-toggle="dropdown" aria-expanded="false"><li class="li-search">${nombreSolo}</li></a>
                        <ul class="dropdown-menu" style="z-index:1000">
                            <li><a class="dropdown-item" href="${url1}">Trabajador</a></li>
                            <li><a class="dropdown-item" href="${url2}">Editar</a></li>
                            <li><a class="dropdown-item" href="${url3}">Horario</a></li>
                            
                        </ul></div>`;
                    break;
                    // Antes
                    // <li><a class="dropdown-item" href="/trabajador/${id}/licencias" target="_blank">Licencias</a></li>
                    //         <li><a class="dropdown-item" href="/trabajador/${id}/perfil_justificantes" target="_blank">Justificantes</a></li>
            }
        });
        searchWrapper.classList.add("active");
        showSuggestions(emptyArray);
    } else {
        searchWrapper.classList.remove("active");
    }
}
function clickeado() {
    let userData = inputBox.value;
    if (userData) {
        searchWrapper.classList.remove("active"); //hide autocomplete box
    }
}
inputBox.addEventListener('click', clickeado, false);

function showSuggestions(list) {
    let listData;
    if (!list.length) {
        userValue = inputBox.value;
        listData = `<li>No se han encontrado resultados</li>`;
    } else {
        listData = list.join('');
    }
    suggBox.innerHTML = listData;
}

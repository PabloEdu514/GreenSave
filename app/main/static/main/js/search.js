let trabajadores = ["MADRES"];
let respuesta;

$.ajax({
    type: "get",
    url: "/busqueda",
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
                case "MADRES":
                    return data = `<a href="/trabajadorasmadres"><li class="li-search">${data}</li></a>`
                    break;

                default:
                    id = 0;
                    respuesta.forEach(element => {
                        if (element.nombre == data) {
                            id = element.id
                        }
                    });
                    return data = `<div class="dropdown nav-item"><a href="#" data-bs-toggle="dropdown" aria-expanded="false"><li class="li-search">${data}</li></a>
                        <ul class="dropdown-menu" style="z-index:1000">
                            <li><a class="dropdown-item" href="/trabajador/${id}/">Trabajador</a></li>
                            <li><a class="dropdown-item" href="/editartrabajador/${id}">Editar</a></li>
                            <li><a class="dropdown-item" href="/perfil_horario/${id}/false/">Horario</a></li>
                            <li><a class="dropdown-item" href="/trabajador/${id}/licencias" target="_blank">Licencias</a></li>
                            <li><a class="dropdown-item" href="/trabajador/${id}/perfil_justificantes" target="_blank">Justificantes</a></li>
                        </ul></div>`;
                    break;
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

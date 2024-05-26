const userDataScript = document.getElementById('user-data');
const userId = userDataScript.dataset.userId;

let dataTable;
let dataTableInitialized=false;
let contador = 0;
const dataTableOptions = {
    searching: false,
    paging: true, // Habilita la paginación
    pagingType: "full_numbers", // Utiliza la paginación completa
    lengthChange: false, // Desactiva la opción de cambiar la cantidad de entradas por página
    pageLength: 30, // Define la cantidad de datos por página
    ordering: false,
    info: false,
    destroy: true,
    language: {
        paginate: {
            first: '', // Deja en blanco el texto para el botón "First"
            previous: '<i class="fas fa-chevron-left"></i>', // Icono para el botón "Anterior"
            next: '<i class="fas fa-chevron-right"></i>', // Icono para el botón "Siguiente"
            last: '' // Deja en blanco el texto para el botón "Last"
        }
    }
};



function limitarDescripcion(descripcion, limitePalabras) {
    // Convertir la descripción a cadena de texto
    const descripcionString = descripcion.toString();
    const palabras = descripcionString.split(' ');
    if (palabras.length > limitePalabras) {
        return palabras.slice(0, limitePalabras).join(' ') + '...';
    } else {
        return descripcionString;
    }
}


const initDataTable=async ()=>{

    if(dataTableInitialized){
        dataTable.destroy();
    }

    await listSolicitudes();
    
    dataTable=$('#Tabla-Solicitudes').DataTable(dataTableOptions);
    dataTableInitialized=true;  
        
    }



const listSolicitudes = async () => {
    try {
        const response = await fetch(`/dep_mantenimiento/CargarSolicitudes/${userId}`);

        const data = await response.json();
        let content = '';
        data.solicitudes.forEach((solicitudes, index) => {
            // checamos el tiempo transcurrido de la solicitud para mostrar o no los botones de editar y eliminar
            const hideButtons = solicitudes.tiempo_transcurrido > 3600;
            let icono;
            switch (solicitudes.status) {
                case 'En_proceso':
                    icono = '<i id="En_proceso" class="fa-solid fa-circle-play" style="color: #1B396B ;font-size: 30px;"></i>'; // Icono de "play" cuando el estado es "En proceso"
                    break;
                case 'Realizado':
                    icono = '<i id="Realizado" class="fa-solid fa-circle-check" style="color: #1B396B ;font-size: 30px;"></i>'; // Icono de "check" cuando el estado es "Completado"
                    break;
                case 'En_espera':
                    icono = '<i id="En_espera" class="fa-solid fa-circle-pause" style="color: #1B396B ;font-size: 30px;"></i>';
                    break;             
                case 'Pendiente':
                    icono = '<i id="Pendiente" class="fa fa-clock-o" aria-hidden="true" style="color: #1B396B;font-size: 30px;"></i>'; 
                    break;
                case 'Rechazado':
                    icono = '<i id="Rechazado" class="fa-solid fa-circle-xmark" style="color: #1B396B;font-size: 30px; "></i>';
                    break;
                case 'Enviado':
                    icono = '<i id="Enviado" class="fa fa-envelope" aria-hidden="true" style="color: #1B396B;font-size: 30px; "></i> ';
                    break;
                case 'Solicitud_Firmada':
                    icono = '<i id="Firmado" class="fa fa-file-signature" aria-hidden="true" style="color: #1B396B;font-size: 30px; "></i> ';
                    break;      
                    
                default:
                    icono = solicitudes.status; // Usa el texto del estado como icono por defecto
            }
            // limitar la descripción a 10 palabras y agregar puntos suspensivos
            const descripcionLimitada = limitarDescripcion(solicitudes.descripcion, 10);
            let botones;
            if (solicitudes.firma_Jefe_Departamento == false) {
                botones = !hideButtons ? `
                <a class="btn btn-sm-2" style="background-color: #1a759f !important;" href="/dep_mantenimiento/Formulario/Docente/Solicitud/${solicitudes.id}" role="button" onclick="event.stopPropagation()">
                    <i class="fa fa-pencil-square" aria-hidden="true" style="color: #ffffff !important;"></i>
                </a>
                <a class="btn btn-sm-2" style="background-color: #d90429 !important;" role="button"  onclick="showDeleteAlert(${solicitudes.id}); event.stopPropagation();">
                    <i class="fa fa-trash" aria-hidden="true" style="color: #ffffff !important;"></i>
                </a>
                ` : `
                <button class="btn btn-sm-2" style="background-color: #6c757d !important;" onclick="showTimeLimitAlert(); event.stopPropagation();">
                    <i class="fa fa-lock" style="color: #ffffff !important;" aria-hidden="true"></i>
                </button>
                `;
            } else {
                botones = `
                <button class="btn btn-sm-2" style="background-color: #6c757d !important;" onclick="showTimeLimitAlert(); event.stopPropagation();">
                    <i class="fa fa-lock" style="color: #ffffff !important;" aria-hidden="true"></i>
                </button>
                `;
            }


            
            if (solicitudes.ocultar==false) { // Verifica si la solicitud no está oculta
                 // Incrementa el contador
                contador++;
                content += `
                    <tr onclick="openDetalle(${solicitudes.id})" class="${solicitudes.status}">
                        <td scope="row"  class="index">${contador}</td>
                        <td class ="servicio">${solicitudes.tipo_servicio}</td>
                        <td class ="descripcion">${descripcionLimitada}</td>
                        <td class ="botones">
                           ${botones}
                        </td>
                        <td class ="status">${icono}</td> <!-- Aquí se mostrará el icono correspondiente -->
                        <td class ="fecha">${solicitudes.fecha}</td>
                    
                        <td class ="hora">${solicitudes.hora}</td>
                    </tr>


                `;
            }
        });
        tbodySolicitudes.innerHTML = content;
        
        
        
    } catch (e) {
        alert(e);
    }
};


// Función para mostrar la alerta
function showTimeLimitAlert() {
    Swal.fire({
        icon: 'info',
        title: '¡Alerta!',
        text: 'Has superado el tiempo límite para editar esta solicitud.',
        confirmButtonText: 'Aceptar'
    });
}

function showDeleteAlert(solicitudId) {
// Mostrar un toast de confirmación
Swal.fire({

    icon: 'warning',
    title: '¿Estás seguro de que quieres borrar esta Solicitud?',
    showCancelButton: true,
    confirmButtonText: 'Aceptar',
    cancelButtonText: 'Cancelar'
}).then((result) => {
    // Si el usuario hace clic en "Aceptar", redirige a la URL con el ID de la solicitud
    if (result.isConfirmed) {
        window.location.href = `/dep_mantenimiento/eliminar-solicitud/${solicitudId}`;
    }
});


}




function openDetalle(solicitudId) {
   
    window.location.href = `/dep_mantenimiento/Docente/Ver_Solicitud/${solicitudId}/` ;

}

const reloadDataTable = async () => {
    await initDataTable(); // Llama a la función para inicializar la tabla DataTable nuevamente
};
const reloadFilDataTable = async () => {
    await initDataTable(); // Llama a la función para inicializar la tabla DataTable nuevamente
    const filtro = document.getElementById('Filtro').value;
    filterTable(filtro);
};



// Función para filtrar la tabla
const filterTable = (filtro) => {
    const tbody = document.querySelector('#Tabla-Solicitudes tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const originalRows = Array.from(tbody.querySelectorAll('tr')); // Almacena una copia de las filas originales
    if (filtro === 'Recientes') {
        tbody.innerHTML = ''; // Limpiar el tbody antes de agregar las filas en el nuevo orden
        rows.forEach(row => tbody.prepend(row)); // Agregar las filas en orden original (Nuevo a Viejo)
    } else if (filtro === 'Pasadas') {
        tbody.innerHTML = ''; // Limpiar el tbody antes de agregar las filas en el nuevo orden
        rows.reverse().forEach(row => tbody.appendChild(row)); // Agregar las filas en orden inverso (Viejo a Nuevo)
    } else {
        rows.forEach(row => {
            const status = row.querySelector('.status').querySelector('i').id; // Obtener el ID del icono dentro de la celda de estado
            const servicio = row.querySelector('.servicio').textContent.trim();

            // Muestra la fila si el filtro es "todos" o coincide con el servicio o el estado
            if (filtro === 'todos' || servicio === filtro || status === filtro) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
};







window.addEventListener('load', async () => {
    await initDataTable();

    // Agrega un evento de escucha al campo de búsqueda externo para filtrar los resultados de la tabla
    $('#searchInput').on('keyup', function () {
        const searchText = this.value.toLowerCase();
        const rows = document.querySelectorAll('#Tabla-Solicitudes tbody tr');

        rows.forEach(row => {
            const columns = row.querySelectorAll('td');
            let found = false;

            columns.forEach(column => {
                const text = column.textContent.toLowerCase();
                if (text.includes(searchText)) {
                    found = true;
                }
            });

            if (found) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });

    // Agrega un evento de escucha al campo del filtro para filtrar los resultados de la tabla
    $('#Filtro').on('change', function () {
        const filtro = document.getElementById('Filtro').value;
        filterTable(filtro);
    });






});

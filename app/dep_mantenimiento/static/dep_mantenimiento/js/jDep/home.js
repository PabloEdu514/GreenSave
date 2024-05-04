const userDataScript = document.getElementById('user-data');
const userId = userDataScript.dataset.userId;

let dataTable;
let dataTableInitialized=false;

const dataTableOptions = {
    searching: false,
    paging: false,
    ordering: false,
    info: false,
    
    destroy: true
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
        const response = await fetch(`/dep_mantenimiento/CargarSolicitudesJdep/${userId}`);

        const data = await response.json();
        let content = '';
        data.solicitudes.forEach((solicitudes, index) => {
            // checamos el tiempo transcurrido de la solicitud para mostrar o no los botones de editar y eliminar
            const hideButtons = solicitudes.tiempo_transcurrido > 3600;
            let icono;
            switch (solicitudes.status) {
                case 'En proceso':
                    icono = '<i id="En proceso" class="fa-solid fa-circle-play" style="color: #1B396B "></i>'; // Icono de "play" cuando el estado es "En proceso"
                    break;
                case 'Realizado':
                    icono = '<i id="Realizado" class="fa-solid fa-circle-check" style="color: #1B396B "></i>'; // Icono de "check" cuando el estado es "Completado"
                    break;
                case 'En espera':
                    icono = '<i id="En espera" class="fa-solid fa-circle-pause" style="color: #1B396B "></i>';
                    break;             
                case 'Pendiente':
                    icono = '<i id="Pendiente" class="fa fa-clock-o" aria-hidden="true" style="color: #1B396B"></i>'; 
                    break;
                case 'Rechazado':
                    icono = '<i id="Rechazado" class="fa-solid fa-circle-xmark" style="color: #1B396B "></i>';
                    break;
                case 'Enviado':
                    icono = '<i id="Enviado" class="fa fa-envelope" aria-hidden="true" style="color: #1B396B "></i> ';
                    break;                
                default:
                    icono = solicitudes.status; // Usa el texto del estado como icono por defecto
            }
            let nombreTrabajadorHTML = ''; // Inicializa la variable para almacenar el HTML del nombre del trabajador
    
            if (solicitudes.nombre_completo_trabajador) {
                // Si la solicitud tiene un trabajador asociado, muestra el nombre del trabajador
                nombreTrabajadorHTML = `By: ${solicitudes.nombre_completo_trabajador}`;
            }

            content += `
                <tr onclick="openDetalle(${solicitudes.id})" class="${solicitudes.status}">
                    <td scope="row"  class ="texto">${index + 1}</td>
                    <td class ="servicio">${solicitudes.tipo_servicio}</td>
                    <td class ="descripcion">${solicitudes.descripcion}</td>
                    <td class ="Trabajador">${nombreTrabajadorHTML}</td> <!-- Mostrar el nombre del trabajador -->
                    <td class ="botones">
                        ${!hideButtons ? `
                        <button  class="btn btn-sm-2"  onclick="editSolicitud(${solicitudes.id}, event)">   
                        <i class="fa fa-pencil-square" aria-hidden="true" style="color: #1B396B !important"></i>
                        
                        </button>
                        <button  class="btn  btn-sm-2" data-bs-toggle="modal" data-bs-target="#exampleModal">
                    
                        <i class="fa fa-trash" aria-hidden="true" style="color: #1B396B !important" ></i>
                        </button>

                        <!-- Modal -->
                        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="exampleModalLabel">Eliminar Solicitud </h1>
                                <button  class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <p>¿Quieres eliminar la solicitud ${solicitudes.id}?</p>
                            </div>
                            <div class="modal-footer">
                                <button   data-bs-dismiss="modal">Cancelar</button>
                                <a class="btn btn-danger" href="/dep_mantenimiento/eliminar-solicitud/${solicitudes.id}/">Eliminar</a>

                            </div>
                            </div>
                        </div>
                        </div>
                    ` : ''}
                    </td>
                    <td class ="status">${icono}</td> <!-- Aquí se mostrará el icono correspondiente -->
                    <td class ="fecha">${solicitudes.fecha}</td>
                   
                    <td class ="hora">${solicitudes.hora}</td>
                </tr>


            `;

        });
        tbodySolicitudes.innerHTML = content;
        
        
        
    } catch (e) {
        alert(e);
    }
};

function editSolicitud(solicitudId, event) {
    event.stopPropagation();
    // Lógica para editar la solicitud
}

function eliminarSolicitud(solicitudId) {
    // Realizar la eliminación de la solicitud utilizando fetch, AJAX u otra técnica de tu elección
    fetch(`/dep_mantenimiento/eliminar-solicitud/${solicitudId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Asegúrate de enviar el token CSRF
        },
    })
    .then(response => {
        if (response.ok) {
            // Recargar la tabla de solicitudes después de eliminar una solicitud
            reloadDataTable();
        } else {
            throw new Error('No se pudo eliminar la solicitud.');
        }
    })
    .catch(error => {
        console.error('Error al eliminar la solicitud:', error);
    });
}




// Función para obtener el valor de la cookie CSRF
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function openDetalle(solicitudId) {
   
    // Redirige a la página HTML deseada con el ID de la solicitud
    //window.location.href = `/detalle_solicitud.html?id=${solicitudId}`;
     // Mostrar una alerta con los detalles de la solicitud
     alert(`Le diste clic a la solicitud: ${solicitudId}
     `);
     console.log('Detalles de la solicitud:', solicitudId);

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

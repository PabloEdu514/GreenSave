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
        const response = await fetch(`/dep_mantenimiento/CargarSolicitudes/${userId}`);

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


            content += `
                <tr onclick="openDetalle(${solicitudes.id})" class="${solicitudes.status}">
                    <td class ="texto">${index + 1}</td>
                    <td class ="servicio">${solicitudes.tipo_servicio}</td>
                    <td class ="descripcion">${solicitudes.descripcion}</td>
                    <td class ="botones">
                        ${!hideButtons ? `
                        <button class="btn btn-sm-1"  onclick="editSolicitud(${solicitudes.id})">   
                        <i class="fa fa-pencil-square" aria-hidden="true" style="color: #1B396B !important"></i>
                        
                        </button>
                        <button class="btn btn-sm-1" onclick="confirmDelete(${solicitudes.id})">
                    
                        <i class="fa fa-trash" aria-hidden="true" style="color: #1B396B !important"></i>
                        </button>
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

const userDataScript = document.getElementById('user-data');
const userId = userDataScript.dataset.userId;

let dataTable;
let dataTableInitialized=false;

const dataTableOptions = {
    searching: false,
    paging: true, // Habilita la paginación
    pagingType: "full_numbers", // Utiliza la paginación completa
    lengthChange: false, // Desactiva la opción de cambiar la cantidad de entradas por página
    pageLength: 2, // Define la cantidad de datos por página
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
        const response = await fetch(`/dep_mantenimiento/CargarSolicitudesJdep/${userId}`);

        const data = await response.json();
        let content = '';
        data.solicitudes.forEach((solicitudes, index) => {
            // checamos el tiempo transcurrido de la solicitud para mostrar o no los botones de editar y eliminar
            const hideButtons = solicitudes.tiempo_transcurrido > 3600;
            let icono;
            switch (solicitudes.status) {
                case 'En_proceso':
                    icono = '<i id="En_proceso" class="fa-solid fa-circle-play" style="color: #1B396B "></i>'; // Icono de "play" cuando el estado es "En proceso"
                    break;
                case 'Realizado':
                    icono = '<i id="Realizado" class="fa-solid fa-circle-check" style="color: #1B396B "></i>'; // Icono de "check" cuando el estado es "Completado"
                    break;
                case 'En_espera':
                    icono = '<i id="En_espera" class="fa-solid fa-circle-pause" style="color: #1B396B "></i>';
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
            // Limitar la descripción a 10 palabras y agregar puntos suspensivos
            const descripcionLimitada = limitarDescripcion(solicitudes.descripcion, 10);
            // Chequeamos si hay un trabajador asociado a la solicitud
            const nombreTrabajador = solicitudes.nombre_completo_trabajador ? solicitudes.nombre_completo_trabajador : 'N/A';
            // Botón o icono dependiendo del estado de la firma del jefe de departamento
            let actionElement;
            if (solicitudes.firmado_jefe_departamento==true) {
                actionElement = '<i class="fa fa-check-circle" style="color: green;"></i>';
            } else {
                actionElement = `<button class="btn btn-sm btn-primary" onclick="enviarSolicitudFirmaJefeDepartamento(${solicitudes.id})">Firmar</button>`;
            }
            content += `
                <tr onclick="openDetalle(${solicitudes.id})" class="${solicitudes.status}">
                    <td scope="row"  class ="texto">${index + 1}</td>
                    <td class ="servicio">${solicitudes.tipo_servicio}</td>
                    <td class="descripcion" ${!solicitudes.nombre_completo_trabajador ? 'colspan="2"' : ''}>${descripcionLimitada}</td>
                    ${solicitudes.nombre_completo_trabajador ? `<td class="Pertenece">De: ${nombreTrabajador}</td>` : ''}
                    <td class ="botones">
                        ${!hideButtons ? `
                        <button  class="btn btn-sm-2" style="background-color: #1a759f !important;" onclick="editSolicitud(${solicitudes.id}, event)">   
                        <i class="fa fa-pencil-square" aria-hidden="true" style=" color: #ffffff !important;"></i>
                        
                        </button>
                        <button  class="btn  btn-sm-2" data-bs-toggle="modal" style="background-color: #d90429 !important;" data-bs-target="#exampleModal">
                    
                        <i class="fa fa-trash" aria-hidden="true" style=" color: #ffffff !important;" ></i>
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
                    <td class ="Firmado">                     ${actionElement}                    </td>
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


// Función para enviar la solicitud de firma al jefe de departamento

const enviarSolicitudFirmaJefeDepartamento = async (solicitudId) => {
    try {
        // Realiza una solicitud POST para enviar la solicitud de firma al jefe de departamento
        const response = await fetch(`/FirmarSolicitud/Jefe_Departamento/${solicitudId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Agrega el token CSRF a las cabeceras
            }
        });
        if (response.ok) {
            // Si la solicitud se envió correctamente, actualiza la interfaz cambiando el botón por un icono de check
            const row = document.querySelector(`#Tabla-Solicitudes tbody tr[data-id="${solicitudId}"]`);
            row.querySelector('.Firmado').innerHTML = '<i class="fa fa-check-circle" style="color: green;"></i>';
        } else {
            throw new Error('Error al enviar la solicitud de firma al jefe de departamento');
        }
    } catch (error) {
        console.error(error);
        alert('Error al enviar la solicitud de firma al jefe de departamento');
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

const userDataScript = document.getElementById('user-data');
const userId = userDataScript.dataset.userId;

let dataTable;
let dataTableInitialized=false;

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

const initDataTable = async () => {
    if(dataTableInitialized){
        dataTable.destroy();
    }

    await listSolicitudes();
    
    dataTable=$('#Tabla-Solicitudes').DataTable(dataTableOptions);
    dataTableInitialized=true;  
};

const listSolicitudes = async () => {
    try {
        const response = await fetch(`/dep_mantenimiento/CargarSolicitudesJefeMantenimiento/${userId}`);
        const data = await response.json();
        let content = '';
        data.solicitudes.forEach((solicitudes, index) => {
           
            let icono;
            switch (solicitudes.status) {
                case 'En_proceso':
                    icono = '<i id="En proceso" class="fa-solid fa-circle-play" style="color: #1B396B ;font-size: 30px;"></i>'; // Icono de "play" cuando el estado es "En proceso"
                    break;
                case 'Realizado':
                    icono = '<i id="Realizado" class="fa-solid fa-circle-check" style="color: #1B396B ;font-size: 30px;"></i>'; // Icono de "check" cuando el estado es "Completado"
                    break;
                case 'En_espera':
                    icono = '<i id="En espera" class="fa-solid fa-circle-pause" style="color: #1B396B ;font-size: 30px;"></i>';
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
                default:
                    icono = solicitudes.status; // Usa el texto del estado como icono por defecto
            }
            // Limitar la descripción a 10 palabras y agregar puntos suspensivos
            const descripcionLimitada = limitarDescripcion(solicitudes.descripcion, 10);
            // Botón o icono dependiendo del estado de la firma del empleado
            let actionElement;
            if (solicitudes.firmado_empleado === true) {
                actionElement = `
                <button class="btn btn-sm-2" style="background-color: #6a994e !important;">   
                <i class="fa fa-check-square" style="color: #ffffff;  font-size: 25px ; text-align: center "></i>
                </button>`;
            } else {
                actionElement = `<button class="btn btn-sm-2" style="background-color: #118ab2 !important;" onclick="fimarSolicitud(${solicitudes.id}, event)">   
                                    <i class="fa fa-pencil-square-o" style="color: #ffffff !important; font-size: 25px ;" aria-hidden="true"></i>
                                 </button>`;
            }
            
          
           // Agregamos la información de pertenencia y departamento
            const perteneceInfo = solicitudes.nombre_completo_trabajador ? 
                `De: ${solicitudes.nombre_completo_trabajador}` : 
                `De: ${solicitudes.nombre_completo_jefe_departamento}`;

            const departamentoInfo = solicitudes.nombre_completo_trabajador ? 
                solicitudes.departamento_trabajador : 
                solicitudes.departamento_jefe_departamento;

             // Chequeamos si hay un trabajador asociado a la solicitud
             const nombre_Empleado = solicitudes.nombre_completo_empleado ? `De: ${solicitudes.nombre_completo_empleado}` : 'Sin Empleado Aignado';
           

            content += `
                <tr onclick="openDetalle(${solicitudes.id})" class="${solicitudes.status}">
                    <td scope="row"  class ="index">${index + 1}</td>
                    <td class ="servicio">${solicitudes.tipo_servicio}</td>
                    <td class ="descripcion">${descripcionLimitada}</td>
                  
                    <td class ="Pertenece">${perteneceInfo}</td>
                    <td class ="Departamento">${departamentoInfo}</td>
                    <td class ="Asignado"> ${nombre_Empleado}   </td>
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

function fimarSolicitud(solicitudId, event) {
    event.stopPropagation();
    // Lógica para editar la solicitud
}

// Función para obtener el valor de la cookie CSRF
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function openDetalle(solicitudId) {
    // Mostrar una alerta con los detalles de la solicitud
    alert(`Le diste clic a la solicitud: ${solicitudId}`);
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

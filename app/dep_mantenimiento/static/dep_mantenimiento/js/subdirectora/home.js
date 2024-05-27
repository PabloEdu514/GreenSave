const userDataScript = document.getElementById('user-data');
const userId = userDataScript.dataset.userId;

let dataTable;
let dataTableInitialized=false;
let contador=0;
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
        const response = await fetch(`/dep_mantenimiento/CargarSolicitudesSubdirectora/${userId}`);
        const data = await response.json();
        let content = '';
        data.solicitudes.forEach((solicitudes, index) => {
           // checamos el tiempo transcurrido de la solicitud para mostrar o no los botones de editar y eliminar
           const hideButtons = solicitudes.tiempo_transcurrido > 3600;
            let icono;
            
            // Limitar la descripción a 10 palabras y agregar puntos suspensivos
            const descripcionLimitada = limitarDescripcion(solicitudes.descripcion, 10);
         

            
            
           // Agregamos la información de pertenencia y departamento
            const perteneceInfo = solicitudes.nombre_completo_trabajador ? 
            `De: ${solicitudes.nombre_completo_trabajador}` : 
            solicitudes.nombre_completo_jefe_departamento ? 
            `De: ${solicitudes.nombre_completo_jefe_departamento}` : '';

            // Agregamos la información del departamento
            const departamentoInfo = solicitudes.nombre_completo_trabajador ? 
            solicitudes.departamento_trabajador : 
            solicitudes.departamento_jefe_departamento ? 
            solicitudes.departamento_jefe_departamento : '';
              // Botón o icono dependiendo del estado de la firma del empleado
              let actionElement;
              if ( solicitudes.resolvio === false && perteneceInfo && departamentoInfo && solicitudes.status === 'En_espera' ) {
                actionElement = `

                <a class="btn btn-sm-2" style="background-color: #fca311 !important;"  href="/dep_mantenimiento/Formulario_Peticion/Subdirectora/Solicitud/${solicitudes.id}" role="button">

                  
                <i class="fa fa-exclamation-triangle" style="color: #ffffff;  font-size: 25px ; text-align: center "></i>
                </a>`;
                
                
              }
              else if (solicitudes.resolvio === true && perteneceInfo && departamentoInfo && solicitudes.status === 'Enviado' ) {
                actionElement = `

                

                <button class="btn btn-sm-2" style="background-color: #6a994e !important;" onclick="showResolvioPeticion(); event.stopPropagation();">   
                <i class="fa fa-check-square" style="color: #ffffff;  font-size: 25px ; text-align: center "></i>
                </button>`;
              }
              
              else if (solicitudes.resolvio === false && !solicitudes.Mat_Rechazo && perteneceInfo && departamentoInfo && solicitudes.status === 'Rechazado' ) {
                actionElement = `
                <button class="btn btn-sm-2" style="background-color: rgba(255, 46, 0, 0.83) !important;" onclick="showRechazoPeticion(); event.stopPropagation();">   
                <i class="fa fa-times-circle" style="color: #ffffff;  font-size: 25px ; text-align: center "></i>
                </button>`;
              }

              else if ( solicitudes.resolvio === false && solicitudes.id_subdirectora && !perteneceInfo && !departamentoInfo && solicitudes.status === 'En_espera' ) {
                actionElement = `

                <a class="btn btn-sm-2" style="background-color: #fca311 !important;"  href="/dep_mantenimiento/Formulario_Peticion/Subdirectora/Solicitud/${solicitudes.id}" role="button">

                  
                <i class="fa fa-exclamation-triangle" style="color: #ffffff;  font-size: 25px ; text-align: center "></i>
                </a>`;
            
             }

             else if ( solicitudes.resolvio === true && solicitudes.id_subdirectora && !perteneceInfo && !departamentoInfo && solicitudes.status === 'En_espera' ) {
                actionElement = `

                <button class="btn btn-sm-2" style="background-color: #6a994e !important;"onclick="showResolvioPeticion(); event.stopPropagation();">   
                <i class="fa fa-check-square" style="color: #ffffff;  font-size: 25px ; text-align: center "></i>
                </button>`;
            
            }


            else if (solicitudes.resolvio === false && !solicitudes.Mat_Rechazo  && !perteneceInfo && !departamentoInfo && solicitudes.status === 'Rechazado' ) {
                actionElement = `
                <button class="btn btn-sm-2" style="background-color: rgba(255, 46, 0, 0.83) !important;" onclick="showRechazoPeticion(); event.stopPropagation();">   
                <i class="fa fa-times-circle" style="color: #ffffff;  font-size: 25px ; text-align: center "></i>
                </button>`;
              }



              
              else {
                actionElement = !hideButtons ? `
                    <a class="btn btn-sm-2" style="background-color: #1a759f !important;" href="/dep_mantenimiento/Formulario/Subdirectora/Solicitud/${solicitudes.id}" role="button">
                        <i class="fa fa-pencil-square" aria-hidden="true" style=" color: #ffffff !important;"></i>
                    </a>
                    <a class="btn btn-sm-2" style="background-color: #d90429 !important;" role="button"  onclick="showDeleteAlert(${solicitudes.id}); event.stopPropagation();">

                    <i class="fa fa-trash" aria-hidden="true" style=" color: #ffffff !important;" ></i>
                    </a>
                    
                    
                ` : `
                    <button  class="btn  btn-sm-2"  style="background-color: #6c757d !important;" onclick="showTimeLimitAlert(); event.stopPropagation();">
                        <i class="fa fa-lock" style=" color: #ffffff !important;" aria-hidden="true"></i>
                    </button>
                `;
            }
            
            // Si ambos perteneceInfo y departamentoInfo están presentes, mostrar el icono de alerta
            if (perteneceInfo && departamentoInfo && solicitudes.resolvio === false && solicitudes.status === 'En_espera' ) {
                icono = '<i id="Alerta" class="fa fa-exclamation-triangle" style="color: #fca311; font-size: 30px;"></i>';
            }
            else if (perteneceInfo && departamentoInfo && solicitudes.resolvio === false && solicitudes.status === 'Rechazado' ) {
                icono = '<i id="Rechazado" class="fa-solid fa-circle-xmark" style="color: #1B396B;font-size: 30px; "></i>';
            
            }


            else{
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
                    case 'Solicitud_Firmada':
                        icono = '<i id="Firmado" class="fa fa-file-signature" aria-hidden="true" style="color: #1B396B;font-size: 30px; "></i> ';
                        break;                    
                    default:
                        icono = solicitudes.status; // Usa el texto del estado como icono por defecto
                }

            }

            let BotonVobo;
            if ( solicitudes.firmado_jefe_departamento === true  && solicitudes.firmaEmpleados === true && solicitudes.firmaVobo === false && solicitudes.status==="Solicitud_Firmada") {
                BotonVobo = `
                <a class="btn btn-sm-2" style="background-color: #9a8c98 !important;" href="/dep_mantenimiento/Firmar_Formulario_VoBo/Subdirectora/Solicitud/${solicitudes.id}" role="button">
                <i class="fa fa-pencil-square-o" style="color: #ffffff;  font-size: 25px ; text-align: center "></i>
                </a>
                `;
                
              }
            else if (solicitudes.firmado_jefe_departamento === true  && solicitudes.firmaEmpleados === true && solicitudes.firmaVobo === true && solicitudes.status==="Realizado") {
                BotonVobo = `
                <button class="btn btn-sm-2" style="background-color: #6a994e !important;"onclick="showSolicitudFirmada(); event.stopPropagation();">   
                <i class="fa fa-check-square" style="color: #ffffff;  font-size: 25px ; text-align: center "></i>
                </button>`;
              }
            
            else {
                BotonVobo = `

                `;
            }  
             


           
        if (solicitudes.ocultar==false) { // Verifica si la solicitud no está oculta
                 // Incrementa el contador
                
            contador++;
            content += `
                <tr onclick="openDetalle(${solicitudes.id})" class="${solicitudes.status}" >
                    <td scope="row"  class="index">${contador}</td>
                    <td class ="servicio">${solicitudes.tipo_servicio}</td>
                    <td class ="descripcion">${descripcionLimitada}</td>
                  
                    <td class ="Pertenece">${perteneceInfo}</td>
                    <td class ="Departamento">${departamentoInfo}</td>
                    <td class ="botones">
                    ${actionElement}
                    ${BotonVobo}
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

function editSolicitud(solicitudId, event) {
    window.location.href = `/dep_mantenimiento/Formulario/Subdirectora/Solicitud/${solicitudId}/` ;
}

function peticionSolicitud(solicitudId, event) {
    window.location.href = `/dep_mantenimiento/Formulario_Peticion/Subdirectora/Solicitud/${solicitudId}/` ;
}


function showResolvioPeticion() {
    Swal.fire({
        icon: 'succes',
       
        title: 'Solicitud resuelta',
        text: 'La solicitud ha sido atendida y resuelta satisfactoriamente.',
        confirmButtonText: 'Aceptar'
    });
}


function showRechazoPeticion() {
    Swal.fire({
        icon: 'error',
        title: 'Solicitud rechazada',
        text: 'La solicitud ha sido rechazada. Por favor, revise los detalles de la solicitud.',
        confirmButtonText: 'Aceptar'
    });
}




function openDetalle(solicitudId) {
   
    window.location.href = `/dep_mantenimiento/Subdirectora/Ver_Solicitud/${solicitudId}/` ;

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

    // Función para mostrar la alerta
function showTimeLimitAlert() {
    Swal.fire({
        icon: 'info',
        title: '¡Alerta!',
        text: 'Has superado el tiempo límite para editar esta solicitud.',
        confirmButtonText: 'Aceptar'
    });
}
function showSolicitudFirmada() {
    Swal.fire({
        icon: 'success',
        title: 'La solicitud ya ha sido firmada.',
        
        confirmButtonText: 'Aceptar'
    });
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

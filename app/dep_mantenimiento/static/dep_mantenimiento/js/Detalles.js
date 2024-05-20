// Recibimos el id de la solicitud del script de la página.
const userDataScript = document.getElementById('solicitud_id');
const solicitudId = userDataScript.dataset.solicitudId; // Cambio: solicitudId en lugar de solicitudid

// Esta función se encarga de cargar y mostrar el historial de solicitudes
async function cargarHistorial(solicitudId) {
    try {
        // Hacemos una solicitud AJAX para obtener los datos del historial de solicitudes
        const response = await fetch(`/dep_mantenimiento/CargarSolicitudDetallada/${solicitudId}/`);

        if (!response.ok) {
            throw new Error('Error al obtener los datos del historial de solicitudes');
        }
        const data = await response.json();
        const historial = data.historial;
        let icono;
        let información;

        // Creamos un HTML con los datos del historial y lo agregamos al contenedor
        const historialHTML = historial.map(item => {
            // Definimos el icono y la información según el estado del historial
            if (item.nuevo_status === 'Enviado') {
                icono = '<i class="fa fa-envelope" aria-hidden="true" style="color: #1B396B;font-size: 30px;"></i>';
              
                if (data.solicitud.nombre_trabajador) {
                    información = `Se envió la solicitud por ${data.solicitud.nombre_trabajador}`;
                } 
                else if(data.solicitud.nombre_jefe){
                    información = `Se envió la solicitud por ${data.solicitud.nombre_jefe}`;
                }
                else {
                    información = `La solicitud fue firmada por ${data.solicitud.nombre_subdirectora}`;
                }





            } else if (item.nuevo_status === 'Solicitud_firmada') {
                icono = '<i class="fa fa-file-signature" aria-hidden="true" style="color: #1B396B;font-size: 30px;"></i>';
                if (data.solicitud.firma_Jefe_Departamento) {
                    información = `La solicitud fue firmada por ${data.solicitud.nombre_jefe}`;
                } else {
                    información = `La solicitud fue firmada por ${data.solicitud.nombre_subdirectora}`;
                }
            } else if (item.nuevo_status === 'Empleado_asignado') {
                icono = '<i class="fa-solid fa-circle-play" style="color: #1B396B;font-size: 30px;"></i>';
                información = `Se asignó al empleado ${data.solicitud.nombre_Empleado}`;
            } else if (item.nuevo_status === 'Firmado por el Empleado') {
                icono = '<i class="fa fa-file-signature" aria-hidden="true" style="color: #1B396B;font-size: 30px;"></i>';
                información = `El empleado ${data.solicitud.nombre_Empleado} firmó la solicitud`;
            } else if (item.nuevo_status === 'Servicio Realizado') {
                icono = '<i class="fa fa-check-circle" aria-hidden="true" style="color: #1B396B;font-size: 30px;"></i>';
                información = `Se completó el servicio`;
            } else if (item.nuevo_status === 'En espera de solucion') {
                icono = '<i class="fa-solid fa-circle-pause" style="color: #1B396B;font-size: 30px;"></i>';
                información = `Tu solicitud está en espera`;
            } else if (item.nuevo_status === 'Se rechazo la peticion' || item.nuevo_status === 'Se rechazo la solicitud') {
                icono = '<i class="fa fa-times-circle" aria-hidden="true" style="color: #1B396B;font-size: 30px;"></i>';
                información = `Se rechazó la solicitud`;
            } else if (item.nuevo_status === 'Resuelto') {
                icono = '<i class="fa fa-check-circle" aria-hidden="true" style="color: #1B396B;font-size: 30px;"></i>';
                información = `Continúa tu solicitud`;
            }

            // Creamos un HTML para cada elemento del historial
            return `
            <div class="historial-item">
                <div class="row align-items-center">
                    <div class="col-md-auto">
                        <div class="icono">${icono}</div>
                    </div>
                    <div class="col-lg-8">
                        <div class="row">
                            <label class="form-label sm-1" style="font-weight: bold; color: #99344C;"  >${información}</label>
                            <label class="form-label md-3">${item.fecha}</label>
                            <label class="form-label md-3">${item.hora}</label>      
                        </div>
                    </div>
                </div>
            </div>`;
        }).join('');

        // Mostramos el historial en el contenedor
        mostrarHistorial(historialHTML);
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Función para mostrar el historial en el contenedor
function mostrarHistorial(historialHTML) {
    const historialContainer = document.getElementById('historial-container');
    if (historialContainer) {
        historialContainer.innerHTML = historialHTML;
    } else {
        console.error('No se encontró el contenedor del historial en la página.');
    }
}

// Llamamos a la función cargarHistorial cuando se haya cargado completamente la página
window.addEventListener('load', async () => {
    // Llamamos a cargarHistorial pasando el ID de la solicitud
    await cargarHistorial(solicitudId);
});

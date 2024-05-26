function Descargarpdf(solicitud_id) {
    const url = `/generar-pdf/${solicitud_id}/`;
    
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/pdf',
        },
    })
    .then(response => response.blob())
    .then(blob => {
        const link = document.createElement('a');
        const url = window.URL.createObjectURL(blob);
        link.href = url;
        link.download = `solicitud_${solicitud_id}.pdf`;
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error al descargar el PDF:', error));
}

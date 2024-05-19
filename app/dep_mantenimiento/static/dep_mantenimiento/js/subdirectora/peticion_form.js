document.addEventListener('DOMContentLoaded', function() {
    const desRechazo = document.getElementById('desRechazo');
    const desResuelto = document.getElementById('desResuelto');
    const rechazoButton = document.getElementById('Rechazo');

    window.aparecerCampo = function() {
        desRechazo.style.display = 'block';
        rechazoButton.style.display = 'none';
        desResuelto.style.display = 'none';
    };
});

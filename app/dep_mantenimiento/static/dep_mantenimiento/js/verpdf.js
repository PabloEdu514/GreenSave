 // URL del PDF generado
 var pdfUrl = "{% url 'generar_pdf' solicitud_id=solicitud.id %}";
        
 // Cargar el PDF usando PDF.js
 var loadingTask = pdfjsLib.getDocument(pdfUrl);
 loadingTask.promise.then(function(pdf) {
     // Obtener la primera página del PDF
     pdf.getPage(1).then(function(page) {
         // Escalar el contenido del PDF
         var scale = 1.5;
         var viewport = page.getViewport({ scale: scale });

         // Obtener el lienzo del visor de PDF
         var canvas = document.getElementById('pdf-viewer');
         var context = canvas.getContext('2d');
         canvas.height = viewport.height;
         canvas.width = viewport.width;

         // Renderizar la página en el lienzo
         var renderContext = {
             canvasContext: context,
             viewport: viewport
         };
         page.render(renderContext);
     });
 });
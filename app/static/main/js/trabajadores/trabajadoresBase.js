$(document).ready(function(){
   $("#example1").DataTable({
      responsive: true, 
      lengthChange: false, 
      autoWidth: false,
      buttons: ["copy", "csv", "excel", "pdf", "print"],
      language: {
         url: '//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json'
     }
    }).buttons().container().appendTo('#example1_wrapper .col-md-6:eq(0)');
});


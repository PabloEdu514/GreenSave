 $(function () {

     $("#directivos").DataTable({
       "responsive": true, "lengthChange": false, "autoWidth": false,
       "buttons": ["copy", "csv", "excel", "pdf", "print", "colvis"]
     }).buttons().container().appendTo('#directivos_wrapper .col-md-6:eq(0)');

   });

   function asignarIdDepto(id){

       console.log("hola mundo")

       $("#idasignacion").val(id).change();

   }
// permet de changer les informations en fonction de la localisation
function local(id_localisation){
    $.post('http://localhost:8000/index/sortie/changementloc',
    {
        id_localisation: id_localisation,
    }, function(data) {
        $(id_localisation).html(data);
    });
}

// Permet de mettre en actif le bouton de la navbar du header
$(document).ready(function () {
  $(".nav li").removeClass("active");
  $('#page_sortie').addClass('active');
});

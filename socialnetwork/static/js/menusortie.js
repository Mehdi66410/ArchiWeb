/* 
* Cette fonction permet de renvoyer l'id_localisation a la vue changementloc afin de pouvoir modifier la variable localisation
* 
*/
function local(id_localisation){
    $.post('http://localhost:8000/sortie/changementloc',
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

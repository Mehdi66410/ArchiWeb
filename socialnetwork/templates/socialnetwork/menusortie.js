$(document).ready(function(){   // le document est chargé
     $(".avis-cadre-texte-afficher-a").click(function(){  // on selectionne tous les liens et on donne une action quand on clique dessus
    var page=($(this).attr("href")); // on recuperer l' adresse du lien
    window.curentLink = $(this);
    $.ajax({
        url: page,
        cache: false,
        })
    .done(function(hmtl) {  window.curentLink.parents("#avis-cadre-texte-ligne").next("#contenu").html(hmtl);   })
    .fail(function(XMLHttpRequest, textStatus, errorThrows) {   alert("error "); })
    .always(function() { /*alert("complete");*/ })
     return false; // on desactive le lien
    });
});
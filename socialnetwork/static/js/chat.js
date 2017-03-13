// Met le bouton envoyer en mode grisé si le user ne tape aucun message
// empeche l'envoie de message vide
$(document).ready(function() {
     $('#send').attr('disabled','disabled');
     $('#chat-msg').keyup(function() {
        if($(this).val() != '') {
           $('#send').removeAttr('disabled');
        }
        else {
        $('#send').attr('disabled','disabled');
        }
     });
 });

// scroll en bas à chaque fois dans le chat
$(document).ready(function () {
	element = document.getElementById('div_scroll');
	element.scrollTop = element.scrollHeight;
});

// Permet de mettre en actif le bouton de la navbar du header
$(document).ready(function () {
  $(".nav li").removeClass("active");
  $('#page_affinite').addClass('active');
});



/**
 * Cette fonction permet de pouvoir mettre j'aime à une personne, on récupère l'id de la personne sur laquelle on veut mettre j'aime et on appelle la vue jaime
 * pour réaliser le traitement, ensuite on renvoit les informations sur la prochaine personne présenté
 */
function like(id_perso){
    $.post('http://localhost:8000/jaime',
    {
        id_perso : id_perso
    }, function(data) {
        if(data=="Aucun profil n'a été trouvé, n'hésitez pas a réessayer plus tard."){
            $("#okok").text(data);
        }
        else{
            var obj = JSON.parse(data);
            $("#nom-"+ id_perso).html(obj.nom);
            $("#genre-"+ id_perso).html(obj.genre);
            $("#age-"+ id_perso).html(obj.age);
            $("#loc-"+ id_perso).html(obj.loc);
            $("#pro-"+ id_perso).html(obj.pro);
            $("#desc-" + id_perso).html(obj.desc);
            document.getElementById('imageUser').src=obj.pic; 
        }
    });
}
/**
 * Cette fonction permet de pouvoir mettre j'aime pas à une personne, on récupère l'id de la personne sur laquelle on veut mettre j'aime pas et on appelle la vue jaime
 * pour réaliser le traitement, ensuite on renvoit les informations sur la prochaine personne présenté
 */
function dislike(id_perso){
	$.post('http://localhost:8000/jaimepas',
    {
        id_perso : id_perso
    }, function(data) {
        if(data=="Aucun profil n'a été trouvé, n'hésitez pas a réessayer plus tard."){
            $("#okok").text(data);
        }
        else{
            var obj = JSON.parse(data);
            $("#nom-"+ id_perso).html(obj.nom);
            $("#genre-"+ id_perso).html(obj.genre);
            $("#age-"+ id_perso).html(obj.age);
            $("#loc-"+ id_perso).html(obj.loc);
            $("#pro-"+ id_perso).html(obj.pro);
            $("#desc-" + id_perso).html(obj.desc);
            document.getElementById('imageUser').src=obj.pic; 
        }
    });
}

// Permet de mettre en actif le bouton de la navbar du header
$(document).ready(function () {
  $(".nav li").removeClass("active");
  $('#page_rencontre').addClass('active');
});

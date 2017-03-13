function like(id_perso){

    $.post('http://localhost:8000/index/jaime',
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

function dislike(id_perso){
	$.post('http://localhost:8000/index/jaimepas',
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
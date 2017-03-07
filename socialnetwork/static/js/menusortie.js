function local(id_localisation){
    $.post('http://localhost:8000/index/sortie/changementloc',
    {
        id_localisation: id_localisation,
    }, function(data) {
        $(id_localisation).html(data);
    });
}

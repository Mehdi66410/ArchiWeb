function like(id_like){
    $.post('http://localhost:8000/index/sortie/ajoutlike',
    {
        id_like: id_like,
    }, function(data) {
		$("#"+id_like).html(data);
	});
}

function dislike(id_like){
	$.post('http://localhost:8000/index/sortie/ajoutdislike',
    {
        id_like: id_like,
    }, function(data) {
		$("#"+id_like).html(data);
	});
}

function present(id_bar){
    $.post('http://localhost:8000/index/sortie/present',
    {
        id_bar: id_bar,
    }, function(data) {
        $("#"+id_bar).html(data);
    });
}
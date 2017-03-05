function like(id_like,barname){
    $.post('http://localhost:8000/index/sortie/ajoutlike',
    {
        barname: barname,
    }, function(data) {
		$("#"+id_like).html(data);
	});
}

function dislike(id_like,barname){
	$.post('http://localhost:8000/index/sortie/ajoutdislike',
    {
        barname: barname,
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
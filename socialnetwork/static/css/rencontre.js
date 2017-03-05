function genre_person(genre_){
    $.post('http://localhost:8000/index/rencontre/genre_person',
    {
        genre_: genre_,
    }, function(data) {
        $(genre_).html(data);
    });
}
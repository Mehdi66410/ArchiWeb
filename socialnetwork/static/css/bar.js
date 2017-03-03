// $(document).ready(function(){
  // $('#1').click(function() { 


  // 	alert('Fonctionne');
  // });

  function coucou(id_like, barname){
  	//alert('Fonctionne' + id_like);

    // $.ajaxSetup({
    //     headers: { "X-CSRFToken": getCookie("csrftoken") }
    // });

    $.post('http://localhost:8000/index/sortie/ajoutjaime',
    {
        barname: barname,
    }, function(data) {
        console.log(data);
		$("#"+id_like).html(data);


	});

  }
// });
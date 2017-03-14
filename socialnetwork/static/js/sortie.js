/*
* Cette fonction utiliser afin de pouvoir récupérer la liste des personne présente en fonction de l'id_disco
 */
function present_person(id_place,place){
    if(place=='disco'){
      $.post('http://localhost:8000/personne_present_disco',
      {
          id_place: id_place,
      }, function(data) {
          $("#affichage_pers-" + id_place).text(data);
      });
    }else if(place=='bar'){
      $.post('http://localhost:8000/personne_present_bar',
      {
          id_place: id_place,
      }, function(data) {
          $("#affichage_pers-" + id_place).text(data);
      });
    }else if(place=='resto'){
      $.post('http://localhost:8000/personne_present_restau',
      {
          id_place: id_place,
      }, function(data) {
          $("#affichage_pers-" + id_place).text(data);
      });
    }
}
/**
 * Cette fonction permet de remplir la table presentDisco en ajoutant l'id disco et l'id de la personne connecté
 */
function present(id_place,place){
  if(place=='disco'){
    $.post('http://localhost:8000/presentdisco',
      {
          id_place: id_place,
      });
  }else if(place=='bar'){
    $.post('http://localhost:8000/present',
        {
            id_place: id_place,
        });
  }else if(place=='resto'){
    $.post('http://localhost:8000/presentrestau',
    {
        id_place: id_place,
    });
  }
  alert("Votre enregistrement est pris en compte!")
}
/**
 * Ces fonctions sont utilisé pour afficher les 5 étoiles (notes du bar/restaurant/discothèque)
 */
var __slice = [].slice;
(function($, window) {
  var Starrr;

  Starrr = (function() {
    Starrr.prototype.defaults = {
      rating: void 0,
      numStars: 5,
      change: function(e, value) {}
    };

    function Starrr($el, options) {
      var i, _, value_star,_ref,
        _this = this;

      this.options = $.extend({}, this.defaults, options);
      this.$el = $el;
      _ref = this.defaults;
      for (i in _ref) {
        _ = _ref[i];
        if (this.$el.data(i) != null) {
          this.options[i] = this.$el.data(i);
        }
      }
      this.createStars();
      this.syncRating();
      this.$el.on('mouseover.starrr', 'span', function(e) {
        return _this.syncRating(_this.$el.find('span').index(e.currentTarget) + 1); //ici
      });
      this.$el.on('mouseout.starrr', function() {
        return _this.syncRating();
      });
      this.$el.on('click.starrr', 'span', function(e) {
        var value = _this.$el.find('span').index(e.currentTarget) + 1;
        var id_place = _this.$el.data('id');
        var place = _this.$el.data('place');
        if(place=='disco'){
          $.post('http://localhost:8000/starsDisco',
          {
              value: value,
              id_place: id_place
          }, function(data) {
              $("#count-existing-" + id_place).text(data);
          });
        }else if(place=='bar'){
          $.post('http://localhost:8000/stars',
          {
            value: value,
            id_place: id_place
          }, function(data) {
            $("#count-existing-" + id_place).text(data);
          });
        }else if(place=='resto'){
          $.post('http://localhost:8000/starsRestau',
          {
              value: value,
              id_place: id_place
          }, function(data) {
              $("#count-existing-" + id_place).text(data);
          });
        }
        return _this.setRating(_this.$el.find('span').index(e.currentTarget) + 1);
      });
      this.$el.on('starrr:change', this.options.change);

    }

    Starrr.prototype.createStars = function() {
      var _i, _ref, _results;

      _results = [];
      for (_i = 1, _ref = this.options.numStars; 1 <= _ref ? _i <= _ref : _i >= _ref; 1 <= _ref ? _i++ : _i--) {
        _results.push(this.$el.append("<span class='glyphicon .glyphicon-star-empty'></span>"));
      }
      return _results;
    };

    Starrr.prototype.setRating = function(rating) {
      if (this.options.rating === rating) {
        rating = void 0;
      }
      this.options.rating = rating;
      this.syncRating();
      return this.$el.trigger('starrr:change', rating);
    };

    Starrr.prototype.syncRating = function(rating) {
      var i, _i, _j, _ref;

      rating || (rating = this.options.rating);
      if (rating) {
        for (i = _i = 0, _ref = rating - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
          this.$el.find('span').eq(i).removeClass('glyphicon-star-empty').addClass('glyphicon-star');
        }
      }
      if (rating && rating < 5) {
        for (i = _j = rating; rating <= 4 ? _j <= 4 : _j >= 4; i = rating <= 4 ? ++_j : --_j) {
          this.$el.find('span').eq(i).removeClass('glyphicon-star').addClass('glyphicon-star-empty');
        }
      }
      if (!rating) {
        return this.$el.find('span').removeClass('glyphicon-star').addClass('glyphicon-star-empty');
      }
    };

    return Starrr;

  })();
  return $.fn.extend({
    starrr: function() {
      var args, option;

      option = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
      return this.each(function() {
        var data;

        data = $(this).data('star-rating');
        if (!data) {
          $(this).data('star-rating', (data = new Starrr($(this), option)));
        }
        if (typeof option === 'string') {
          return data[option].apply(data, args);
        }
      });
    }
  });
})(window.jQuery, window);

$(function() {
  return $(".starrr").starrr();
});

$( document ).ready(function() {
      
  $('#stars').on('starrr:change', function(e, value){
    $('#count').html(value);
  });
  
  $('#stars-existing').on('starrr:change', function(e, value){
    $('#count-existing').html(value);
  });
});


// permet de switcher entre visible ou non d'un div
function toggle(anId){
  node = document.getElementById(anId);
  if (node.style.display=="none"){
    node.style.display = "";
  }
  else{
    node.style.display = "none";
  }
}

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

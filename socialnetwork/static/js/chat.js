$('#chat-form').on('submit', function(event){
    event.preventDefault();

    $.ajax({
        url : '/post/',
        type : 'POST',
        data : { msgbox : $('#chat-msg').val() },

        success : function(json){
            $('#chat-msg').val('');
            $('#msg-list').append('<li class="text-right list-group-item">' + json.msg + '</li>');
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        }
    });
});

function getMessages(){
    if (!scrolling) {
        $.get('/messages/', function(messages){
            $('#msg-list').html(messages);
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function(){
    $('#msg-list-div').on('scroll', function(){
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 2000);
});

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

var url = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(url);

$('.chat-app-window').scrollTop(Number.MAX_SAFE_INTEGER) // Default window scroll-down
$("input[name=message]").focus()

$(document).ready(function(){

	var form = $( 'form' ).on( 'submit', function(e) {
    	e.preventDefault();
    	var message = $("input[name=message]").val()
		socket.emit( 'my_event', {
	    	msg: message
	    })
	})

    socket.on( 'message_sent', function( data ){
    	$("input[name=message]").val("")
    	$('.chat-app-window').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
    	$('.chats').append('<div class="chat"><div class="chat-body"><div class="chat-content"><p>'+data.msg+'</p></div></div></div>')
    	console.log(data)
    })

});
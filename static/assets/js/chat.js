var url = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(url);

$('.chat-app-window').scrollTop(Number.MAX_SAFE_INTEGER) // Default window scroll-down
$("input[name=message]").focus()

$(document).ready(function(){

	var form = $( 'form' ).on( 'submit', function(e) {
    	e.preventDefault();
    	var message = $("input[name=message]").val()
		socket.emit( 'my_event', {
            student_id: $("input#student_id").val(),
	    	message: message
	    })
	})

    socket.on( 'message_sent', function( data ){
    	$("input[name=message]").val("")
    	$('.chats').append('<div class="chat"><div class="chat-body"><div class="chat-content"><p>'+data.message+'</p></div></div></div>')
    	$('.chat-app-window').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
        let student_messages = $('a[href^="/chat/'+data.student_id+'"]')
        $('#student_messages').prepend(student_messages) // Prepend user messages on top of the list
        student_messages.find("div > p > span#messages-id-"+data.student_id).text(data.message)
        console.log(data)
    })

    socket.on( 'message_received', function( data ){
    	// CHECK IF THAT STUDENT ID IS AN OPEN WINDOW AND THEN DECIDE EITHER TO APPEND TO THE SIDEBAR OR CHAT MESSAGES
    })

});
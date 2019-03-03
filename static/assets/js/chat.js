var url = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(url);

$('.chat-app-window').scrollTop(Number.MAX_SAFE_INTEGER) // Default window scroll-down
$("input[name=message]").focus()

function getCurrentTime(){
    return new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
}

$(document).ready(function(){

	var form = $( 'form' ).on( 'submit', function(e) {
    	e.preventDefault();
    	var message = $("input[name=message]").val()
		socket.emit( 'my_event', {
            student_id: $("input#student_id").val(),
	    	message: message,
            time: getCurrentTime()
	    })
	})

    socket.on( 'message_sent', function( data ){
    	$("input[name=message]").val("")
    	$('.chats').append('<div class="chat"><div class="chat-body"><div class="chat-content"><p>'+data.message+'</p></div></div></div>')
    	$('.chat-app-window').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
        let student_messages = $('a[href^="/chat/'+data.student_id+'"]')
        $('#student_messages').prepend(student_messages) // Prepend user messages on top of the list
        student_messages.find("div > p > span#messages-id-"+data.student_id).text(data.message)
        student_messages.find("div > h6 > span#message-time-"+data.student_id).text(data.time)
    })

    socket.on( 'message_received', function( data ){
        // CHECK if user exists, chat open, chat closed
        let student_messages = $('a[href^="/chat/'+data.student_id+'"]')
        $('#student_messages').prepend(student_messages) // Prepend user messages on top of the list
        student_messages.find("div > p > span#messages-id-"+data.student_id).text(data.message)
        let unread_count = student_messages.find("div > p > span > span#unread_count-"+data.student_id)
        unread_count.html(Number(unread_count.html())+1)
    })

});
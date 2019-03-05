var url = 'https://' + document.domain + ':' + location.port;
var socket = io.connect(url, { transports: ['xhr-polling'] });

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
        let student_messages = $('#student-message-'+data.student_id)
        $('#student_messages').prepend(student_messages) // Prepend user messages on top of the list
        student_messages.find("#messages-id-"+data.student_id).text(data.message)
        student_messages.find("#message-time-"+data.student_id).text(data.time)
    })

    socket.on( 'message_received', function( data ){
        let student_messages = $('#student-message-'+data.student_id) // sidebar object
        let nice_message = data.message; // message that goes on the side panel
        let img_or_message = '<div class="chat-content"><p>'+data.message+'</p></div>' // message that shows up inside the chat

        if (data.is_img == true){  // If message is sent, instead of writing URL, write image
            nice_message = "Image"
            img_or_message = '<div class="chat-content" style="width:20%"><a href="'+$("input#static_url").val()+'/'+data.message+'" target="_blank"><img src="'+$("input#static_url").val()+'/downloads/image_icon.png" width="10%"> Image attachment</a></div>'
        }
        if (data.is_report == true) {
            img_or_message = '<div class="chat-content bg-danger bg-lighten-2"><p>'+data.message+'</p></div>' // report that shows up inside the chat
        }

        if (student_messages.text() == ""){
            // CASE WHEN STUDENT DOES NOT EXIST IN THE TAB
            student_messages = '<a href="/chat/'+data.student_id+'" class="media bg-blue-grey bg-lighten-5 border-right-info border-right-2" id="student-message-'+data.student_id+'"><div class="media-left pr-1"><span class="avatar avatar-md"><img class="media-object rounded-circle" src="../static/app-assets/images/portrait/small/avatar-s-3.png"alt="Generic placeholder image"></span></div><div class="media-body w-100"><h6 class="list-group-item-heading">'+data.name+'<span class="font-small-3 float-right info message-time" id="message-time-'+data.student_id+'">'+getCurrentTime()+'</span></h6><p class="list-group-item-text text-muted mb-0"><span id="messages-id-'+data.student_id+'">'+nice_message+'</span><span class="float-right primary" id="unread-wrap-'+data.student_id+'"><span class="badge badge-pill badge-dark" id="unread-count-'+data.student_id+'">1</span></span></p></div></a>'; // student messages that were not in the chat before

        }
        else if ($("input#student_id").val() == data.student_id) {
            // CASE WHEN STUDENT EXISTS AND OPEN
            if (data.is_report == true){
                $('.chats').append('<div class="chat chat-left"><div class="chat-body">'+img_or_message+'</div></div>') // add message on the left side of that chatroom
            }else {$('.chats').append('<div class="chat chat-left"><div class="chat-body">'+img_or_message+'</div></div>')}
            $('.chat-app-window').scrollTop(Number.MAX_SAFE_INTEGER) // Always scroll down when message sent
        }
        else {
            // CASE WHEN STUDENT EXISTS BUT NOT OPEN
            student_messages.attr('class', 'media bg-blue-grey bg-lighten-5 border-right-info border-right-2')
            let unread_wrap = student_messages.find("div > p > span#unread-wrap-"+data.student_id)
            if (unread_wrap.html().trim().length == 0){
                unread_wrap.html('<span class="badge badge-pill badge-dark" id="unread-count-'+data.student_id+'">1</span>')
            }
            else {
                let unread_count = unread_wrap.find("span#unread-count-"+data.student_id)
                unread_count.html(Number(unread_count.html())+1) // increase unread count
            }
            // let unread_count = student_messages.find("div > p > span > span#unread-count-"+data.student_id) //get unread_count element
            
        }
        $('#student_messages').prepend(student_messages) // Prepend user messages on top of the list

        student_messages = $('#student-message-'+data.student_id) // recreate student_messages object
        student_messages.find("div > p > span#messages-id-"+data.student_id).text(nice_message) // update message on the sidebar
        student_messages.find("div > h6 > span#message-time-"+data.student_id).text(getCurrentTime()) // update time with the current one

    })

});
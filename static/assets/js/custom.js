var url = 'https://' + document.domain + ':' + location.port;
var socket = io.connect(url, { transports: ['websocket', 'polling'] });

function getCurrentTime(){
    return new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
}

$(document).ready(function(){

    socket.on( 'add_message_to_header', function( data ){
    	$("#header-messages").prepend('<a href="/chat/'+data.student_id+'"><div class="media"><div class="media-left"><span class="avatar avatar-sm avatar-online rounded-circle"><img src="'+url+'/static/app-assets/images/portrait/small/avatar-s-19.png" alt="avatar"></span></div><div class="media-body"><h6 class="media-heading">'+data.name+'</h6><p class="notification-text font-small-3 text-muted">'+data.message+'</p><small><time class="media-meta text-muted">'+getCurrentTime()+'</time></small></div></div></a>')
    	$("#header-message-count").html(Number($("#header-message-count").html())+1)
    	$("#no-unread-reader").remove()
        var sound = new Howl({
            src: ['https://instant-notification-system.herokuapp.com/downloads/audio/iphone_receive_sms.mp3.mp3'];
        });
        sound.play();
    });

    socket.on( 'add_report_to_header', function( data ){
    	$("#header-reports").prepend('<a href="/chat/'+data.student_id+'"><div class="media"><div class="media-left align-self-center"><i class="ft-file icon-bg-circle bg-danger"></i></div><div class="media-body"><h6 class="media-heading red darken-1">'+data.name+'</h6><p class="notification-text font-small-3 text-muted">'+data.message+'</p><small><time class="media-meta text-muted">'+getCurrentTime()+'</time></small></div></div></a>')
    	$("#header-report-count").html(Number($("#header-report-count").html())+1)
    	$("#no-reports").remove()
        // $("#notif_sound").trigger('play'); // notification sound
    });

});
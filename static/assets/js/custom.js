var url = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(url);

$(document).ready(function(){

    socket.on( 'add_message_to_header', function( data ){
        console.log("Add new message to header"+data);
    });

});
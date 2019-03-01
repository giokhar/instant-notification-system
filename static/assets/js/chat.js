var url = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(url);



  var form = $( 'form' ).on( 'submit', function( e ) { // when user sends a message invoke socketio for back-end
    e.preventDefault();
    socket.emit( 'my_event', {
    })
  })
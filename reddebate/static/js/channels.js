var socket = new WebSocket('ws://' + window.location.host + '/stocks/');

socket.onopen = function open() {
  console.log('WebSockets connection created.');
};

socket.onmessage = function message(event) {
  console.log("data from socket:" + event.data);
  var table = document.getElementById('chat');
  var row = table.insertRow(0);
  var cell1 = row.insertCell(0);
  cell1.innerHTML = event.data;
};

if (socket.readyState == WebSocket.OPEN) {
  socket.onopen();
}
function start(){
  var msj = document.getElementById('example').value;
  socket.send(msj);
}
function stop() {
  socket.send('stop');
}

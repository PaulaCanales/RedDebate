// var socket = new WebSocket('ws://' + window.location.host + '/stocks/');
//
// socket.onopen = function open() {
//   console.log('WebSockets connection created.');
// };
//
// socket.onmessage = function message(event) {
//   console.log("data from socket:" + event.data);
//   var table = document.getElementById('chat');
//   var row = table.insertRow(0);
//   var cell1 = row.insertCell(0);
//   cell1.innerHTML = event.data;
// };
//
// if (socket.readyState == WebSocket.OPEN) {
//   socket.onopen();
// }
// function start(){
//   var msj = document.getElementById('example').value;
//   socket.send(msj);
// }
// function stop() {
//   socket.send('stop');
// }
// $(function() {
$(document).ready(function(){
  var socket = new WebSocket('ws://' + window.location.host + '/stocks/');
  console.log("channels.js");
  socket.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var debates = $("#Tabla_DbtAbiertos")
        var ele = $('<tr></tr>')

        ele.append(
            $("<td width=300 ></td>").text(data.titulo)
        )
        ele.append(
            $("<td width=600><p></p></td>").text(data.descripcion)
        )

        debates.append(ele)
    };

  $("#nuevodebateform").on("submit", function(event) {
          var message = {
              titulo: $('#debTituloForm').val(),
              descripcion: $('#debDescripcionForm').val(),
              alias_c: $('#debAliasForm').val(),
              largo: $('#debLargoForm').val(),
              num_rebate: $('#debRebateForm').val(),
              date_fin: $('#debFinForm').val(),
              img: $('#debImgForm').val(),
              id_usuario_id: ""
          }
          console.log("submit form debate");
          console.log(message);
          socket.send(JSON.stringify(message));
          // $("#message").val('').focus();
          $("#nuevodebate").slideUp("slow");
          return false;
      });
  });
// }

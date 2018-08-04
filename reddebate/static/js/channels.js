$(document).ready(function(){
  var socket = new ReconnectingWebSocket('ws://' + window.location.host + window.location.pathname);
  socket.onmessage = function(message) {
        var data = JSON.parse(message.data);
        console.log("onmassage");
        if (data.titulo){
          var debates = $("#Tabla_DbtAbiertos")
          var ele = $('<tr></tr>')

          ele.append(
              $("<td width=300 ></td>").text(data.titulo)
          )
          ele.append(
              $("<td width=600><p></p></td>").text(data.descripcion)
          )

          debates.append(ele)
        }
        else if (data.descripcion){
          var data = JSON.parse(message.data);
          var nuevosArgs = $("#alertaArgumento"+data.postura);
          var nuevo = $('<a onclick="javascript:location.reload()" id="nuevoArgumento{{postura}}" class="list-group-item"> </a>').text("Nuevo argumento de "+data.nombre)
          nuevosArgs.append(nuevo)
        }
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
    socket.send(JSON.stringify(message));
    $("#nuevodebate").slideUp("slow");
    return false;
  });

  $("#nuevoArgForm1").on("submit", function(event){
    var message = {
      descripcion: $('#descArg').val(),
      alias_c: $('#aliasArg').val(),
      id_debate: $('#idDebate').val(),
      postura: "",
      id_usuario_id: ""
    }
    socket.send(JSON.stringify(message));
    setTimeout(function(){location.reload();}, 500);
    return false;
  });
});

$(document).ready(function(){
  var socket = new ReconnectingWebSocket('ws://' + window.location.host + window.location.pathname);
  var socket_notificacion = new ReconnectingWebSocket('ws://' + window.location.host + '/notificacion/');

  socket_notificacion.onmessage = function(notificacion){
    console.log("probando notificacion");
    var data = JSON.parse(notificacion.data);
    console.log(data);
    var id_usr_actual = $("#id_usuario_actual").text();
    if (id_usr_actual == data){
      $("#num_notif").text("!")
    }
  };
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
        else if (data.postura_f || data.postura_c){
          var porcentaje_f = Math.round(parseFloat(data.porc_f)*100)/100;
          var porcentaje_c = Math.round(parseFloat(data.porc_c)*100)/100;
          $("#label_porc_f").text(porcentaje_f+"%")
          $("#label_porc_c").text(porcentaje_c+"%")
          $("#label_num_post1").text(data.postura_f)
          $("#label_num_post0").text(data.postura_c)

        }
        else if (data.descripcion){
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
  $("#bot_af_init").click(function(event){
    var message = {
      postura: 1,
      postura_inicial: 1,
      id_usuario: "",
      id_debate: $('#idDebate').val(),
    };
    socket.send(JSON.stringify(message));
    setTimeout(function(){location.reload();}, 500);
    return false;
  });
  $("#bot_ec_init").click(function(event){
    var message = {
      postura: 0,
      postura_inicial: 0,
      id_usuario: "",
      id_debate: $('#idDebate').val(),
    };
    socket.send(JSON.stringify(message));
    setTimeout(function(){location.reload();}, 500);
    return false;
  });
  $("#bot_cambiar_post").click(function(event){
    var message = {
      postura: $('#postura_debate').val(),
      id_debate: $('#idDebate').val(),
      razon: $( "input[name='razon']:checked" ).val(),
    };
    socket.send(JSON.stringify(message));
    setTimeout(function(){location.reload();}, 500);
    return false;
  });

});

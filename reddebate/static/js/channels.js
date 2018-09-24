$(document).ready(function(){
  var socket = new ReconnectingWebSocket('ws://' + window.location.host + window.location.pathname);
  var socket_notificacion = new ReconnectingWebSocket('ws://' + window.location.host + '/notificacion/');

  socket_notificacion.onmessage = function(notificacion){
    var data = JSON.parse(notificacion.data);
    var id_usr_actual = $("#id_usuario_actual").text();
    if (id_usr_actual == data.id_owner){
      $("#alertaSpan").css('color', '#d9534f');
      $("#numSpan").text("");
      $("#numSpan").append($('<span class="glyphicon glyphicon-asterisk" aria-hidden="true"></span>'));
      $("#numSpan").css('background-color', '#d9534f');
      var menu = $("#mySidenav");
      var url = "/debate/"+data.id_debate+"/"+data.id_notification;
      var item = document.getElementById("notificacion"+data.id_notification);
      if(item){
        $("#notificacion"+data.id_notification).hide()
      }
      var ele = $('<li id="notificacion{{notificacion.id}}" class="notificacion0"></li>');
      ele.append($('<a href="'+url+'"></a>').text(data.message));
      menu.prepend(ele);
    }
  };
  socket.onmessage = function(message) {
        var id_usr_actual = $("#id_usuario_actual").text();
        var data = JSON.parse(message.data);
        console.log("onmassage");
        var url = "/debate/"+data.id+"/"
        if (data.title){
          $("#alertaDeb0").css("display","block");
        }
        if (data.members){
          console.log(data.members);
          id_usr = data.members
          for (i=0 ; i<id_usr.length ; i++){
            if (id_usr[i] == id_usr_actual){
              $("#alertaDeb1").css("display","block");
            }
          }
          // var id_usr_actual = $("#id_usuario_actual").text();
          // if (id_usr_actual == data.members){
          //   $("#alertaDeb1").css("display","block");
          // }

        }
        else if (data.infavor_position || data.against_position){
          var infavor_percent = Math.round(parseFloat(data.infavor_percent)*100)/100;
          var against_percent = Math.round(parseFloat(data.against_percent)*100)/100;
          $("#label_porc_f").text(infavor_percent+"%")
          $("#label_porc_c").text(against_percent+"%")
          $("#label_num_post1").text(data.infavor_position)
          $("#label_num_post0").text(data.against_position)

        }
        else if (data.text){
          var nuevosArgs = $("#alertaArgumento"+data.position);
          var nuevo = $('<a onclick="javascript:location.reload()" id="nuevoArgumento'+data.position+'" class="list-group-item"> </a>').text("Nuevo argument de "+data.name)
          nuevosArgs.append(nuevo)
        }
    };

  $("#nuevodebateform").on("submit", function(event) {
    var enddate = $('#debEndDateForm').val()
    if (enddate.length === 0){
      var enddate = null;
    }
    var selected = [];
    if ($('#debMemberTypeForm').val()==1){
      $("input[name*='members']:checked").each(function() {
          selected.push($(this).val());
      });
    }
    else if ($('#debMemberTypeForm').val()==2){
      $("input[name*='listado']:checked").each(function() {
          selected.push($(this).val());
      });
      console.log(selected);
    }

    var message = {
      title: $('#debTitleForm').val(),
      text: $('#debTextForm').val(),
      owner_type: $('#debAliasForm').val(),
      length: $('#debLengthForm').val(),
      args_max: $('#debArgsForm').val(),
      counterargs_max: $('#debCounterArgForm').val(),
      counterargs_type: $('#debCounterArgTypeForm').val(),
      members_type: $('#debMemberTypeForm').val(),
      position_max: $('#debChangePositionForm').val(),
      end_date: enddate,
      id_user_id: "",
      members: selected,
      tags: $("#tagsForms").tagsinput('items'),
    }
    console.log(message);
    socket.send(JSON.stringify(message));
    window.location.reload();
    return false;
  });

  $("#nuevoArgForm1").on("submit", function(event){
    console.log();("a favor")
    var message = {
      text: $('#descArg1').val(),
      owner_type: $('#aliasArg1').val(),
      id_debate: $('#idDebate').val(),
      position: "",
      id_user_id: ""
    }
    socket.send(JSON.stringify(message));
    setTimeout(function(){location.reload();}, 500);
    return false;
  });
  $("#nuevoArgForm0").on("submit", function(event){
    console.log("en contra");
    console.log($('#descArg0').val(),);
    var message = {
      text: $('#descArg0').val(),
      owner_type: $('#aliasArg0').val(),
      id_debate: $('#idDebate').val(),
      position: "",
      id_user_id: ""
    }
    console.log(message);
    socket.send(JSON.stringify(message));
    setTimeout(function(){location.reload();}, 500);
    return false;
  });
  $("#bot_af_init").click(function(event){
    var message = {
      position: 1,
      id_user: "",
      id_debate: $('#idDebate').val(),
    };
    socket.send(JSON.stringify(message));
    setTimeout(function(){location.reload();}, 500);
    return false;
  });
  $("#bot_ec_init").click(function(event){
    var message = {
      position: 0,
      id_user: "",
      id_debate: $('#idDebate').val(),
    };
    socket.send(JSON.stringify(message));
    setTimeout(function(){location.reload();}, 500);
    return false;
  });
  $("#bot_cambiar_post").click(function(event){
    var message = {
      position: $('#postura_debate').val(),
      id_debate: $('#idDebate').val(),
      razon: $( "input[name='razon']:checked" ).val(),
    };
    socket.send(JSON.stringify(message));
    setTimeout(function(){location.reload();}, 500);
    return false;
  });

});

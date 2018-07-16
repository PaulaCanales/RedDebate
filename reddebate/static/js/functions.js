/*
function cambiar_postura(id_debate, postura){
  console.log("funciona .. hasta aqui");
  console.log("debate/"+id_debate)
     $.ajax({

         url: "{% url 'despliega' 1 %}" ,
         type: 'POST',
         data:{  id : id_debate,
                 postura_debate_ajax: postura,
                 csrfmiddlewaretoken: '{{ csrf_token }}'
               } ,
               success: function(data) {
                 document.getElementById('tu_postura').innerHTML = data;
                 console.log(data);
                  if (data == "En Contra"){

                   document.getElementById('bot_ec').style.backgroundColor = '#18BD9B';
                   document.getElementById('bot_ec').style.color = 'WHITE';
                   document.getElementById('bot_af').style.backgroundColor = 'WHITE';
                   document.getElementById('bot_af').style.color = '#18BD9B';

                   if (document.getElementById('form_argumento_afavor').style.display=='none'){
                     document.getElementById('bot_argumento_encontra').style.display = 'block';
                     document.getElementById('bot_argumento_afavor').style.display = 'none';
                   }
                   else
                   {
                     document.getElementById('form_argumento_afavor').style.display = 'none';

                     document.getElementById('bot_argumento_encontra').style.display = 'block';

                   }
                 }
                 else{
                   document.getElementById('bot_af').style.backgroundColor = '#18BD9B';
                   document.getElementById('bot_af').style.color = 'WHITE';
                   document.getElementById('bot_ec').style.backgroundColor = 'WHITE';
                   document.getElementById('bot_ec').style.color = '#18BD9B';

                   if (document.getElementById('form_argumento_encontra').style.display=='none'){
                     document.getElementById('bot_argumento_afavor').style.display = 'block';
                     document.getElementById('bot_argumento_encontra').style.display = 'none';
                   }
                   else
                   {
                     document.getElementById('form_argumento_encontra').style.display = 'none';

                     document.getElementById('bot_argumento_afavor').style.display = 'block';

                   }

                 }

                 if (document.getElementById('argumentos')){
                   // document.getElementById('argumentos').style.display = 'block';
                   $("#argumentos").slideDown("slow");
                   if (num_post_c){
                         if (data == "En Contra"){
                           document.getElementById('num_postura_contra').innerHTML = num_post_c ;
                         }
                         else{
                           document.getElementById('num_postura_favor').innerHTML = num_post_f ;

                         }
                   }
                 }
                 else{
                   if (num_post_c){
                         if (data == "En Contra"){
                           document.getElementById('num_postura_contra').innerHTML = '<span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span> ' + num_post_c;
                           document.getElementById('num_postura_favor').innerHTML = '<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> ' + num_post_f ;
                         }
                         else{
                           document.getElementById('num_postura_favor').innerHTML = '<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> ' + num_post_c ;
                           document.getElementById('num_postura_contra').innerHTML = '<span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span> ' + num_post_f ;
                         }
                    }
                    else{ var relleno =0;}
                 }
               },
               failure: function(data) {
                   alert('Error de conexión');
               },
               crossDomain: true
           });
}
*/
function cambiar_alias(){
  console.log("llega al cambiar_alias");
  document.getElementById('boton_alias').style.display = 'none';
  document.getElementById('formulario_alias').style.display = 'block';
}

function cancelar_alias(){
  console.log("llega al cambiar_alias");
  document.getElementById('formulario_alias').style.display = 'none';
  document.getElementById('boton_alias').style.display = 'block';
}

function formulario_editar_encontra(descripcion){
  console.log("funciona .. hasta aqui editar_contra");
  document.getElementById('textarea4').value = descripcion ;
  document.getElementById('form_editar_encontra').style.display = 'block';
  $("html, body").animate({ scrollTop: $(document).height() }, 1000);
}

function formulario_editar_afavor(descripcion ){
  console.log("funciona .. hasta aqui editar");
  document.getElementById('textarea1').value = descripcion ;
  document.getElementById('form_editar_afavor').style.display = 'block';
  $("html, body").animate({ scrollTop: $(document).height() }, 1000);
}

function rebatir_contra(argumento_id){
  console.log("funciona .. hasta aqui rebatir");
  document.getElementById('argumento_id_rebate_contra').value = argumento_id ;
  document.getElementById('form_rebatir_contra').style.display = 'block';
  $("html, body").animate({ scrollTop: $(document).height() }, 1000);
}

function rebatir_favor(argumento_id){
  console.log("funciona .. hasta aqui rebatir");
  document.getElementById('argumento_id_rebate_favor').value = argumento_id ;
  document.getElementById('form_rebatir_afavor').style.display = 'block';
  $("html, body").animate({ scrollTop: $(document).height() }, 1000);
}

function fomulario_argumento_afavor(){
  console.log("funciona .. hasta aqui");
  document.getElementById('form_argumento_afavor').style.display = 'block';
  document.getElementById('bot_argumento_afavor').style.display = 'none';
}

function fomulario_argumento_encontra(){
  console.log("funciona .. hasta aqui");
  document.getElementById('form_argumento_encontra').style.display = 'block';
  document.getElementById('bot_argumento_encontra').style.display = 'none';
}

function despliega_formulario(id){
  $(id).slideDown("slow");
}

function cierra_formulario(id){
  $(id).slideUp("slow");
}

function formulario_editar_debate(id,id_dbt,titulo,desc,año,mes,dia,alias,largo){
  $(id).slideDown("slow");
  $("html, body").animate({ scrollTop: 0 }, 600);
  document.getElementById('tituloeditar').value = titulo;
  document.getElementById('desceditar').value = desc;
  document.getElementById('iddbteditar').value = id_dbt;

  fecha=año+"-"+mes+"-"+dia
  if (fecha!="--"){
    document.getElementById('fechaeditar').value = fecha; }
  else{
    document.getElementById('fechaeditar').value = null; }
  if (alias=="username"){
    document.getElementById('radio4e').checked= true; }
  else{
    document.getElementById('radio5e').checked= true; }
  if(largo==300){
    document.getElementById('radio1e').checked= true; }
  else if (largo==200){
    document.getElementById('radio2e').checked= true; }
  else{
    document.getElementById('radio3e').checked= true; }
}

function filtrar_debate(myinput,tabla) {
  var input, filter, table, tr, td, i;
  input = document.getElementById(myinput);
  filter = input.value.toUpperCase();
  table = document.getElementById(tabla);
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = ""; }
      else {
        tr[i].style.display = "none"; }
    }
  }
}

function debate_estado(evt, estadoDbt) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none"; }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", ""); }
  document.getElementById(estadoDbt).style.display = "block";
  evt.currentTarget.className += " active";
}
/*
$(document).ready(
  function(){
    try{
      document.getElementById("dbt_abiertos").click(); }
    catch(err){}
  });
*/
function mostrar_historial(modal){
  document.getElementById(modal).style.display="block";
}

function cerrar_historial(modal){
  document.getElementById(modal).style.display="none";
}
/*
function valorar(argumento, id_div, val, opcionusr){
  console.log("llega al valorar");
  console.log(argumento);
  $.ajax({
    url: "{% url 'despliega' 15 %}" ,
    type: 'POST',
    data:{  id_arg : argumento,
      opcion: opcionusr,
      csrfmiddlewaretoken: '{{ csrf_token }}'} ,
      success: function(data) { // id
        document.getElementById(id_div).innerHTML = data;
        document.getElementById(id_div).style.display = "none";
        document.getElementById(val).innerHTML = data;
        document.getElementById(argumento).style.display = 'block';
        console.log("div: ");
        console.log(id_div); },
      failure: function(data) {
        alert('Error de conexión'); },
        crossDomain: true });
}

$(document).ready(function() {
  if (debate.largo){var text_max = debate.largo;}
  else{ var text_max = 0;}
  $('#textarea_feedback1').html(text_max + ' caracteres restantes');
  $('#textarea_feedback2').html(text_max + ' caracteres restantes');
  $('#textarea_feedback3').html(text_max + ' caracteres restantes');
  $('#textarea_feedback4').html(text_max + ' caracteres restantes');
  $('#textarea_feedback5').html(text_max + ' caracteres restantes');
  $('#textarea_feedback6').html(text_max + ' caracteres restantes');

  $('#textarea6').keyup(function() {
    var text_length = $('#textarea6').val().length;
    var text_remaining = text_max - text_length;
    $('#textarea_feedback6').html(text_remaining + ' caracteres restantes'); });

  $('#textarea5').keyup(function() {
    var text_length = $('#textarea5').val().length;
    var text_remaining = text_max - text_length;
    $('#textarea_feedback5').html(text_remaining + ' caracteres restantes'); });

  $('#textarea4').keyup(function() {
    var text_length = $('#textarea4').val().length;
    var text_remaining = text_max - text_length;
    $('#textarea_feedback4').html(text_remaining + ' caracteres restantes'); });

  $('#textarea3').keyup(function() {
    var text_length = $('#textarea3').val().length;
    var text_remaining = text_max - text_length;
    $('#textarea_feedback3').html(text_remaining + ' caracteres restantes'); });

  $('#textarea2').keyup(function() {
    var text_length = $('#textarea2').val().length;
    var text_remaining = text_max - text_length;
    $('#textarea_feedback2').html(text_remaining + ' caracteres restantes'); });

  $('#textarea1').keyup(function() {
    var text_length = $('#textarea1').val().length;
    var text_remaining = text_max - text_length;
    $('#textarea_feedback1').html(text_remaining + ' caracteres restantes'); });
});
*/
/*
google.charts.load('current', {'packages':['corechart','bar']});

// Set a callback to run when the Google Visualization API is loaded.
//if ($('#chart_div').length) {
google.charts.setOnLoadCallback(drawChart_argumento);
google.charts.setOnLoadCallback(drawChart_postura);
google.charts.setOnLoadCallback(drawStuff);

function drawStuff() {
  if (argF[0]){var val_argF1 = argF[0][2]; }
  else{ var val_argF1 =0; }

  if (argF[1]){var val_argF2 = argF[1][2];}
  else{ var val_argF2 =0;}

  if (argC[0]){ var val_argC1 = argC[0][2];}
  else{ var val_argC1 =0; }

  if (argC[1]){ var val_argC2 = argC[1][2]; }
  else { var val_argC2 =0; }

  var data = new google.visualization.arrayToDataTable([
    ['Valoración', 'A Favor','En Contra'],
    ['1º Mejor Valorado', val_argF1 ,val_argC1],
    ['2º Mejor Valorado', val_argF2  , val_argC2], ]);

  var options = {
    width: 800,
    chart: {
      title: 'Valoración',
      subtitle: 'Comparación de los argumentos a favor y en contra más valorados' },
      bars: 'horizontal', // Required for Material Bar Charts.
      series: {
        0: { color: '18BD9B'}, // Bind series 0 to an axis named 'distance'.
        1: { color: '2D3E50'} // Bind series 1 to an axis named 'brightness'.
      },
      axes: {
        x: {
        argumento: {label: 'Valoración'}, // Bottom x-axis.
        valoracion: {side: 'top', label: 'magnitud'} // Top x-axis.
        }
      }
    };

  var chart = new google.charts.Bar(document.getElementById('chart_arg_val'));
  chart.draw(data, options);
 };

   // Callback that creates and populates a data table,
   // instantiates the pie chart, passes in the data and
   // draws it.
   function drawChart_argumento() {

     if (argF){
         var cant_argF =  argF|length;}
     else {
        var cant_argF =0;}
     if (argC){
         var cant_argC =  argC|length;}
     else {
        var cant_argC =0;}
     console.log("cant_argF");
     console.log(cant_argF);
     // Create the data table.
     var data = new google.visualization.DataTable();
     data.addColumn('string', 'Topping');
     data.addColumn('number', 'Slices');
     data.addRows([
       ['A Favor', cant_argF],
       ['En Contra', cant_argC],
     ]);

     // Set chart options
     var options = {'title':'Cantidad de Argumentos en el Debate',
                    'width':400,
                    'height':300,
                    'colors': ['#18BD9B', '#2D3E50']};

     // Instantiate and draw our chart, passing in some options.
     var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
     chart.draw(data, options);
   };

   function drawChart_postura() {

     if (num_post_f > 0){
       var cant_postF = num_post_f;}
     else{
       var cant_postF =0;}
     if (num_post_c > 0){
       var cant_postC = num_post_c;}
     else{
       var cant_postC =0;}
     console.log("cant_postF");
     console.log(cant_postF);
     // Create the data table.
     var data = new google.visualization.DataTable();
     data.addColumn('string', 'Topping');
     data.addColumn('number', 'Slices');
     data.addRows([
       ['A Favor', cant_postF],
       ['En Contra', cant_postC],
     ]);

     // Set chart options
     var options = {'title':'Cantidad de Posturas en el Debate',
                    'width':400,
                    'height':300,
                    'colors': ['#18BD9B', '#2D3E50']};

     // Instantiate and draw our chart, passing in some options.
     var chart = new google.visualization.PieChart(document.getElementById('chart_div2'));
     chart.draw(data, options);
   };
*/

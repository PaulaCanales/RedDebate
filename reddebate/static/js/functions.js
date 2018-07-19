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

function fomulario_argumento(postura){
  document.getElementById('bot_argumento'+postura).style.display = 'none';
  document.getElementById('form_argumento'+postura).style.display = 'block';
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

function mostrar_modal(modal, descripcion, respuesta){
  document.getElementById(modal).style.display="block";
  if (descripcion != 0){
    document.getElementById('textarea1').value = descripcion
  }
  if (respuesta != -1){
    document.getElementById('argumento_id_rebate').value = respuesta ;
  }
}

function cerrar_modal(modal){
  document.getElementById(modal).style.display="none";
}

function definir_postura(id_debate, postura, post_f, post_c){
  if (document.getElementById('argumentos')){
    $("#argumentos").slideDown("slow");
  }
  cambiar_postura(id_debate, postura, post_f, post_c);
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

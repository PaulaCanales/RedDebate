$(function(){
    $('[rel="popover"]').popover({
        container: 'body',
        html: true,
        content: function () {
            var clone = $($(this).data('popover-content')).clone(true).removeClass('hide');
            return clone;
        }
    }).click(function(e) {
        e.preventDefault();
    });
});
function cambiar_alias(){
  document.getElementById('boton_alias').style.display = 'none';
  document.getElementById('formulario_alias').style.display = 'block';
}

function cancelar_alias(){
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
    td = tr[i].getElementsByTagName("td")[2];
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

function mostrar_modal(modal, id_arg, respuestas,postura){
  document.getElementById(modal).style.display="block";
  document.getElementById("id_argumento_rebate"+postura+id_arg).value = id_arg;
};

function cerrar_modal(modal){
  document.getElementById(modal).style.display="none";
}

function definir_postura(id_debate, postura, post_f, post_c){
  if (document.getElementById('argumentos')){
    $("#argumentos").slideDown("slow");
  }
  cambiar_postura(id_debate, postura, post_f, post_c);
}
function confirmar_cambio(post) {
   document.getElementById("cambioPostura_modal").style.display="block";
   document.getElementById("postura_debate").value = post;
}

function ver(evt, estadoDbt) {
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

function borrarFecha(){
  $('#debFinForm').val("")
}

function spinnerReglas(id, operacion, max, min, paso){
  var valor = $('#'+id).val();
  if(operacion>0){
    if(parseInt(valor) < parseInt(max)){
      $('#'+id).val(parseInt(valor)+parseInt(paso));
    }
  }
  else {
    if(parseInt(valor) > parseInt(min)){
      $('#'+id).val(parseInt(valor)-parseInt(paso));
    }
  }

}

// Gráficos

function posturaChart() {
  var data = google.visualization.arrayToDataTable([
          ['Postura', 'Cantidad'],
          ['A Favor', varGlobal.postura_f],
          ['En Contra', varGlobal.postura_c]
        ]);

        var options = {
          title: 'Resumen Posturas',
          width:400,
          height:300,
          colors: ['#18BD9B', '#2D3E50']
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_postura'));
        chart.draw(data, options);
}
function argumentosChart() {
  var data = google.visualization.arrayToDataTable([
          ['Argumentos', 'Cantidad'],
          ['A Favor', varGlobal.argumentos_f],
          ['En Contra', varGlobal.argumentos_c]
        ]);

        var options = {
          title: 'Resumen Argumentos',
          width:400,
          height:300,
          colors: ['#18BD9B', '#2D3E50']
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_argumento'));
        chart.draw(data, options);
}

function cambioPosturaChart() {
  var data = google.visualization.arrayToDataTable([
          ['Cambio', 'Cantidad'],
          ['De Favor a Contra', varGlobal.cambio_favor_contra],
          ['De Contra a Favor', varGlobal.cambio_contra_favor]
        ]);

        var options = {
          title: 'Usuarios que cambiaron de postura: '+varGlobal.cambio_total,
          width:400,
          height:300,
          colors: ['#18BD9B', '#2D3E50']
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_cambioPostura'));
        chart.draw(data, options);

        function selectHandler() {
          var selectedItem = chart.getSelection()[0].row;
         }
        google.visualization.events.addListener(chart, 'select', selectHandler);
}

function mejorArgumentoChart(){
  var data = new google.visualization.arrayToDataTable([
      ['Valoración', 'A Favor','En Contra'],
      ['1º Mejor Valorado', varGlobal.primer_arg_f  ,varGlobal.primer_arg_c],
      ['2º Mejor Valorado', varGlobal.segundo_arg_f  , varGlobal.segundo_arg_c]]);
    var options = {
      title: 'Argumentos a favor y en contra más valorados',
      chartArea: {width: '50%'},
      bars: 'horizontal', // Required for Material Bar Charts.
      series: {
        0: { color: '18BD9B'}, // Bind series 0 to an axis named 'distance'.
        1: { color: '2D3E50'} // Bind series 1 to an axis named 'brightness'.
      },
      hAxis: {
          title: 'Cantidad'
        },
        vAxis: {
          title: 'Valoración'
        }
    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_mejorArgumento'));
    chart.draw(data, options);
   };
function razonCambioChart(){
  var data = new google.visualization.arrayToDataTable([
      ['Razón', 'De Favor a Contra','De Contra a Favor'],
      ['Cambió de opinión', varGlobal.razon_favor_contra[0]  ,varGlobal.razon_contra_favor[0]],
      ['Error de clic', varGlobal.razon_favor_contra[1]  ,varGlobal.razon_contra_favor[1]],
      ['Otro', varGlobal.razon_favor_contra[2] , varGlobal.razon_contra_favor[2]]]);

      var options = {
        title: 'Motivos cambio de postura',
        chartArea: {width: '50%'},
        isStacked: true,
        series: {
          0: { color: '18BD9B'}, // Bind series 0 to an axis named 'distance'.
          1: { color: '2D3E50'} // Bind series 1 to an axis named 'brightness'.
        },
        hAxis: {
          title: 'Cantidad',
          minValue: 0,
        },
        vAxis: {
          title: 'Motivos'
        }
      };
      var chart = new google.visualization.BarChart(document.getElementById('chart_razonCambio'));
      chart.draw(data, options);
    }

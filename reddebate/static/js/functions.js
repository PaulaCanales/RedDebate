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

function mostrar_modal(modal, data){
  document.getElementById(modal).style.display="block";
  document.getElementById('respuestass').textContent = data;
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

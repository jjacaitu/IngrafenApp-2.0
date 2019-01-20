function tipo_trabajo(item) {
  var id = item.options[item.selectedIndex].text
  if (id.slice(-4) == "True"){
    document.getElementById("interiores").style.display = "table-row";

  }else{
    document.getElementById("interiores").style.display = "none";



  }
}


function troquel_existente1_fun(item){
  if(item.value == "Troquel existente" || item.value.slice(-9) == "existente"){
    document.getElementById("troquel_existente1").style.display = "initial";

  }else{
document.getElementById("troquel_existente1").style.display = "none";
document.getElementById("troquel_existente1").value = "";

  }
}

function troquel_existente2_fun(item){
  if(item.value == "Troquel existente" || item.value.slice(-9) == "existente"){
    document.getElementById("troquel_existente2").style.display = "initial";

  }else{
document.getElementById("troquel_existente2").style.display = "none";
document.getElementById("troquel_existente2").value = "";


  }
}

function troquel_existente3_fun(item){
  if(item.value == "Troquel existente" || item.value.slice(-9) == "existente"){
    document.getElementById("troquel_existente3").style.display = "initial";

  }else{
document.getElementById("troquel_existente3").style.display = "none";
document.getElementById("troquel_existente3").value = "";

  }
}

function troquel_existente4_fun(item){
  if(item.value == "Troquel existente" || item.value.slice(-9) == "existente"){
    document.getElementById("troquel_existente4").style.display = "initial";

  }else{
document.getElementById("troquel_existente4").style.display = "none";
document.getElementById("troquel_existente4").value = "";

  }
}

function troquel_existente5_fun(item){
  if(item.value == "Troquel existente" || item.value.slice(-9) == "existente"){
    document.getElementById("troquel_existente5").style.display = "initial";

  }else{
document.getElementById("troquel_existente5").style.display = "none";
document.getElementById("troquel_existente5").value = "";

  }
}

function agregar1() {

  if (document.getElementById('luno').style.display = "none"){
    document.getElementById('luno').style.display = "table-row";
    document.getElementById("material1").required = true;
    document.getElementById("descripcion1").required = true;
    document.getElementById("alto1").required = true;
    document.getElementById("ancho1").required = true;
    document.getElementById("alto1").value = "";
    document.getElementById("ancho1").value = "";
    document.getElementById("troquelado1").required = true;
    document.getElementById("troquelado1").value = "";
    document.getElementById("troqueladh1").value = "";
    document.getElementById("laminado1").required = true;
    document.getElementById("uv1").required = true;
    document.getElementById("impresiont1").required = true;
    document.getElementById("impresionr1").required = true;
    document.getElementById("impresiont1").value = "";
    document.getElementById("impresionr1").value = "";
  }
}

function agregar2() {

  if (document.getElementById('ldos').style.display = "none"){
    document.getElementById('ldos').style.display = "table-row";
    document.getElementById('boton_quitar').style.display = "none";
    document.getElementById("material2").required = true;
    document.getElementById("descripcion2").required = true;
    document.getElementById("alto2").required = true;
    document.getElementById("ancho2").required = true;
    document.getElementById("alto2").value = "";
    document.getElementById("ancho2").value = "";
    document.getElementById("troquelado2").required = true;
    document.getElementById("impresiont2").required = true;
    document.getElementById("impresionr2").required = true;
    document.getElementById("impresiont2").value = "";
    document.getElementById("impresionr2").value = "";
    document.getElementById("troquelado2").value = "";
    document.getElementById("troqueladh2").value = "";
    document.getElementById("uv2").required = true;
    document.getElementById("laminado2").required = true;

  }
}

function agregar3() {

  if (document.getElementById('ltres').style.display = "none"){
    document.getElementById('ltres').style.display = "table-row";
    document.getElementById('boton_quitar2').style.display = "none";
    document.getElementById("material3").required = true;
    document.getElementById("descripcion3").required = true;
    document.getElementById("alto3").required = true;
    document.getElementById("ancho3").required = true;
    document.getElementById("alto3").value = "";
    document.getElementById("ancho3").value = "";
    document.getElementById("troquelado3").required = true;
    document.getElementById("impresiont3").required = true;
    document.getElementById("impresionr3").required = true;
    document.getElementById("impresiont3").value = "";
    document.getElementById("impresionr3").value = "";
    document.getElementById("troquelado3").value = "";
    document.getElementById("troqueladh3").value = "";
    document.getElementById("uv3").required = true;
    document.getElementById("laminado3").required = true;




  }
}

function agregar4() {

  if (document.getElementById('lcuatro').style.display = "none"){
    document.getElementById('lcuatro').style.display = "table-row";
    document.getElementById('boton_quitar3').style.display = "none";
    document.getElementById("material4").required = true;
    document.getElementById("descripcion4").required = true;
    document.getElementById("alto4").required = true;
    document.getElementById("ancho4").required = true;
    document.getElementById("alto4").value = "";
    document.getElementById("ancho4").value = "";
    document.getElementById("troquelado4").required = true;
    document.getElementById("impresiont4").required = true;
    document.getElementById("impresionr4").required = true;
    document.getElementById("impresiont4").value = "";
    document.getElementById("impresionr4").value = "";
    document.getElementById("troquelado4").value = "";
    document.getElementById("troqueladh4").value = "";
    document.getElementById("uv4").required = true;
    document.getElementById("laminado4").required = true;



  }
}
function quitar1() {

  if (document.getElementById('luno').style.display = "table-row"){
    document.getElementById('luno').style.display = "none";
    document.getElementById("material1").required = false;
    document.getElementById("descripcion1").required = false;
    document.getElementById("alto1").required = false;
    document.getElementById("ancho1").required = false;
    document.getElementById("troquelado1").required = false;
    document.getElementById("material1").value = "";
    document.getElementById("descripcion1").value = "";
    document.getElementById("alto1").value = 0;
    document.getElementById("ancho1").value = 0;
    document.getElementById("troquelado1").value = "";
    document.getElementById("impresiont1").value = "";
    document.getElementById("impresionr1").value = "";
    document.getElementById("num_pantonest2").value = "0";
    document.getElementById("num_pantonesr2").value = "0";
    document.getElementById("troquel_existente2").value = "";
    document.getElementById('troqueladoadh1').value = "";
    document.getElementById("impresiont1").required = false;
    document.getElementById("impresionr1").required = false;
    document.getElementById('troqueladoadh1').required = false;
    document.getElementById("uv1").required = false;
    document.getElementById("laminado1").required = false;
    document.getElementById("uv1").value = "";
    document.getElementById("laminado1").value = "";

  }
}

function quitar2() {

  if (document.getElementById('ldos').style.display = "table-row"){
    document.getElementById('ldos').style.display = "none";
    document.getElementById('boton_quitar').style.display = "table-cell";
    document.getElementById("material2").required = false;
    document.getElementById("descripcion2").required = false;
    document.getElementById("alto2").required = false;
    document.getElementById("ancho2").required = false;
    document.getElementById("troquelado2").required = false;
    document.getElementById("material2").value = "";
    document.getElementById("descripcion2").value = "";
    document.getElementById("alto2").value = 0;
    document.getElementById("ancho2").value = 0;
    document.getElementById("troquelado2").value = "";
    document.getElementById("impresiont2").value = "";
    document.getElementById("impresionr2").value = "";
    document.getElementById("num_pantonest3").value = "0";
    document.getElementById("num_pantonesr3").value = "0";
    document.getElementById("troquel_existente3").value = "";
    document.getElementById('troqueladoadh2').value = "";
    document.getElementById("uv2").required = false;
    document.getElementById("laminado2").required = false;
    document.getElementById("impresiont2").required = false;
    document.getElementById("impresionr2").required = false;
    document.getElementById('troqueladoadh2').required = false;
    document.getElementById("uv2").value = "";
    document.getElementById("laminado2").value = "";

  }
}

function quitar3() {

  if (document.getElementById('ltres').style.display = "table-row"){
    document.getElementById('ltres').style.display = "none";
    document.getElementById('boton_quitar2').style.display = "table-cell";
    document.getElementById("material3").required = false;
    document.getElementById("descripcion3").required = false;
    document.getElementById("alto3").required = false;
    document.getElementById("ancho3").required = false;
    document.getElementById("troquelado3").required = false;
    document.getElementById("material3").value = "";
    document.getElementById("descripcion3").value = "";
    document.getElementById("alto3").value = 0;
    document.getElementById("ancho3").value = 0;
    document.getElementById("troquelado3").value = "";
    document.getElementById("uv3").required = false;
    document.getElementById("laminado3").required = false;
    document.getElementById("impresiont3").required = false;
    document.getElementById("impresionr3").required = false;
    document.getElementById('troqueladoadh3').required = false;
    document.getElementById("uv3").value = "";
    document.getElementById("laminado3").value = "";
    document.getElementById("impresiont3").value = "";
    document.getElementById("impresionr3").value = "";
    document.getElementById("num_pantonest4").value = "0";
    document.getElementById("num_pantonesr4").value = "0";
    document.getElementById("troquel_existente4").value = "";
    document.getElementById('troqueladoadh3').value = "";
    document.getElementById('boton_quitar2').style.display = "table-cell";

  }
}

function quitar4() {

  if (document.getElementById('lcuatro').style.display = "table-row"){
    document.getElementById('lcuatro').style.display = "none";
    document.getElementById('boton_quitar3').style.display = "table-cell";
    document.getElementById("material4").required = false;
    document.getElementById("descripcion4").required = false;
    document.getElementById("alto4").required = false;
    document.getElementById("ancho4").required = false;
    document.getElementById("troquelado4").required = false;
    document.getElementById("material4").value = "";
    document.getElementById("descripcion4").value = "";
    document.getElementById("alto4").value = 0;
    document.getElementById("ancho4").value = 0;
    document.getElementById("troquelado4").value = "";
    document.getElementById("uv4").required = false;
    document.getElementById("laminado4").required = false;
    document.getElementById("impresiont4").required = false;
    document.getElementById("impresionr4").required = false;
    document.getElementById('troqueladoadh4').required = false;
    document.getElementById("uv4").value = "";
    document.getElementById("laminado4").value = "";
    document.getElementById("impresiont4").value = "";
    document.getElementById("impresionr4").value = "";
    document.getElementById("num_pantonest5").value = "0";
    document.getElementById("num_pantonesr5").value = "0";
    document.getElementById("troquel_existente5").value = "";
    document.getElementById('troqueladoadh4').value = "";


  }
}

function pantonet1(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonest1").style.display = "initial";
    document.getElementById("num_pantonest1").required = true;
  }else{
document.getElementById("num_pantonest1").style.display = "none";
document.getElementById("num_pantonest1").value = "";
document.getElementById("num_pantonest1").required = false;

  }
}


function pantoner1(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonesr1").style.display = "initial";
    document.getElementById("num_pantonesr1").required = true;

  }else{
document.getElementById("num_pantonesr1").style.display = "none";
document.getElementById("num_pantonesr1").value = "";
document.getElementById("num_pantonesr1").required = false;

  }
}

function pantonet2(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonest2").style.display = "initial";
    document.getElementById("num_pantonest2").required = true;

  }else{
document.getElementById("num_pantonest2").style.display = "none";
document.getElementById("num_pantonest2").value = "";
document.getElementById("num_pantonest2").required = false;

  }
}

function pantoner2(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonesr2").style.display = "initial";
    document.getElementById("num_pantonesr2").required = true;

  }else{
document.getElementById("num_pantonesr2").style.display = "none";
document.getElementById("num_pantonesr2").value = "";
document.getElementById("num_pantonesr2").required = false;

  }
}

function pantonet3(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonest3").style.display = "initial";
    document.getElementById("num_pantonest3").required = true;

  }else{
document.getElementById("num_pantonest3").style.display = "none";
document.getElementById("num_pantonest3").value = "";
document.getElementById("num_pantonest3").required = false;

  }
}

function pantoner3(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonesr3").style.display = "initial";
    document.getElementById("num_pantonesr3").required = true;

  }else{
document.getElementById("num_pantonesr3").style.display = "none";
document.getElementById("num_pantonesr3").value = "";
document.getElementById("num_pantonesr3").required = false;

  }
}

function pantonet4(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonest4").style.display = "initial";
    document.getElementById("num_pantonest4").required = true;

  }else{
document.getElementById("num_pantonest4").style.display = "none";
document.getElementById("num_pantonest4").value = "";
document.getElementById("num_pantonest4").required = false;

  }
}

function pantoner4(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonesr4").style.display = "initial";
    document.getElementById("num_pantonesr4").required = true;

  }else{
document.getElementById("num_pantonesr4").style.display = "none";
document.getElementById("num_pantonesr4").value = "";
document.getElementById("num_pantonesr4").required = false;

  }
}

function pantonet5(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonest5").style.display = "initial";
    document.getElementById("num_pantonest5").required = true;

  }else{
document.getElementById("num_pantonest5").style.display = "none";
document.getElementById("num_pantonest5").value = "";
document.getElementById("num_pantonest5").required = false;

  }
}

function pantoner5(item){
  if(item.value == "Pantones"  || item.value == "F/C + Pantones"){
    document.getElementById("num_pantonesr5").style.display = "initial";
    document.getElementById("num_pantonesr5").required = true;

  }else{
document.getElementById("num_pantonesr5").style.display = "none";
document.getElementById("num_pantonesr5").value = "";
document.getElementById("num_pantonesr5").required = false;

  }
}


function filtros_busqueda(item) {
  if (item.value == "Todo"){
    document.getElementById("parametro").style.display = "none";
    document.getElementById("cl").style.display = "none";
    document.getElementById("tr").style.display = "none";
    document.getElementById("cot").style.display = "none";
    document.getElementById("ven").style.display = "none";
  } else if (item.value == "Cliente") {
    document.getElementById("parametro").style.display = "none";
    document.getElementById("cl").style.display = "initial";
    document.getElementById("tr").style.display = "none";
    document.getElementById("cot").style.display = "none";
    document.getElementById("ven").style.display = "none";

  } else if (item.value == "Trabajo") {
    document.getElementById("parametro").style.display = "none";
    document.getElementById("cl").style.display = "none";
    document.getElementById("tr").style.display = "initial";
    document.getElementById("cot").style.display = "none";
    document.getElementById("ven").style.display = "none";

  }else if (item.value == "Cotizador") {
    document.getElementById("parametro").style.display = "none";
    document.getElementById("cl").style.display = "none";
    document.getElementById("tr").style.display = "none";
    document.getElementById("cot").style.display = "initial";
    document.getElementById("ven").style.display = "none";
  }else if (item.value == "Vendedor") {
    document.getElementById("parametro").style.display = "none";
    document.getElementById("cl").style.display = "none";
    document.getElementById("tr").style.display = "none";
    document.getElementById("cot").style.display = "none";
    document.getElementById("ven").style.display = "initial";
  }else{
    document.getElementById("parametro").style.display = "initial";
    document.getElementById("cl").style.display = "none";
    document.getElementById("tr").style.display = "none";
    document.getElementById("cot").style.display = "none";
    document.getElementById("ven").style.display = "none";
  }

  if(item.value == "Cliente" || item.value == "Vendedor"){
    document.getElementById("b_por_cliente").style.display = "none";
    document.getElementById("b_por_trabajo").style.display = "initial";
    document.getElementById("totales").selected = true;

  }else if (item.value == "Trabajo"){
    document.getElementById("b_por_cliente").style.display = "initial";
    document.getElementById("b_por_trabajo").style.display = "none";
    document.getElementById("totales").selected = true;
  }else{
    document.getElementById("b_por_cliente").style.display = "initial";
    document.getElementById("b_por_trabajo").style.display = "initial";
    document.getElementById("totales").selected = true;
  }
}

function check(){
  var CheckBox = document.getElementById('con_cinta')
  if(CheckBox.checked == true){
    document.getElementById('cantidad_cintas').disabled = false;
    document.getElementById('cm_cintas').disabled = false;
    document.getElementById('tipo_cinta').disabled = false;
    document.getElementById('cantidad_cintas').required = true;
    document.getElementById('cm_cintas').required = true;
    document.getElementById('tipo_cinta').required = true;
  }else{
    document.getElementById('cantidad_cintas').disabled = true;
    document.getElementById('cm_cintas').disabled = true;
    document.getElementById('tipo_cinta').disabled = true;
    document.getElementById('cantidad_cintas').value = "";
    document.getElementById('cm_cintas').value = "";
    document.getElementById('tipo_cinta').value = "";
    document.getElementById('cantidad_cintas').required = false;
    document.getElementById('cm_cintas').required = false;
    document.getElementById('tipo_cinta').required = false;
  }
}

function verificar_tipo_trabajo(item){
  if(document.getElementById(item.value).value == "False"){
    document.getElementById('boton_agregar').style.display = "none";
    document.getElementById("material2").value = "";
    document.getElementById("descripcion2").value = "";
    document.getElementById("alto2").value = "0";
    document.getElementById("ancho2").value = "0";
    document.getElementById("uv2").value = "";
    document.getElementById("laminado2").value = "";
    document.getElementById("troquelado2").value = "";
    document.getElementById("impresiont2").value = "";
    document.getElementById("impresiont2").value = "";
    document.getElementById("material1").value = "";
    document.getElementById("descripcion1").value = "";
    document.getElementById("alto1").value = "0";
    document.getElementById("ancho1").value = "0";
    document.getElementById("uv1").value = "";
    document.getElementById("laminado1").value = "";
    document.getElementById("troquelado1").value = "";
    document.getElementById("impresiont1").value = "";
    document.getElementById("impresionr1").value = "";
    document.getElementById("num_pantonesr3").value = "";
    document.getElementById("num_pantonest3").value = "";
    document.getElementById("num_pantonesr2").value = "";
    document.getElementById("num_pantonest2").value = "";
    document.getElementById('ldos').style.display = "none";
    document.getElementById('luno').style.display = "none";

  }else{
    document.getElementById('boton_agregar').style.display = "table-cell";

  }
  if (document.getElementById(item.value).name != ""){
    document.getElementById("adicional_row").style.display = "table-cell";
    document.getElementById("adicional").placeholder = document.getElementById(item.value).name;
    document.getElementById("adicional_texto").value = document.getElementById(item.value).name;
    document.getElementById("adicional").required = true;
  }else{
    document.getElementById("adicional_row").style.display = "none";
    document.getElementById("adicional").required = false;
    document.getElementById("adicional_texto").value = "";
    document.getElementById("adicional").value = "";
  }


}

function chequeo_material(item){
  if(item.value.slice(0,8) == "Adhesivo"){
    document.getElementById('troqueladoadh').style.display = "initial";
    document.getElementById('troquelado').style.display = "none";
    document.getElementById('troqueladoadh').required = true;
    document.getElementById('troquelado').required = false;
    document.getElementById('troquelado').value = "";
    document.getElementById("impresionr").value = "Sin impresion";
    document.getElementById("impresionr").disabled = true;

  }else{
    document.getElementById('troqueladoadh').style.display = "none";
    document.getElementById('troquelado').style.display = "initial";
    document.getElementById('troquelado').required = true;
    document.getElementById('troqueladoadh').required = false;
    document.getElementById('troqueladoadh').value = "";

    document.getElementById("impresionr").disabled = false;
  }
}

function chequeo_material2(item){
  if(item.value.slice(0,8) == "Adhesivo"){
    document.getElementById('troqueladoadh1').style.display = "initial";
    document.getElementById('troquelado1').style.display = "none";
    document.getElementById('troqueladoadh1').required = true;
    document.getElementById('troquelado1').required = false;
    document.getElementById('troquelado1').value = "";
    document.getElementById("impresionr1").value = "Sin impresion";
    document.getElementById("impresionr1").disabled = true;

  }else{
    document.getElementById('troqueladoadh1').style.display = "none";
    document.getElementById('troquelado1').style.display = "initial";
    document.getElementById('troquelado1').required = true;
    document.getElementById('troqueladoadh1').required = false;
    document.getElementById('troqueladoadh1').value = "";

    document.getElementById("impresionr1").disabled = false;
  }
}

function chequeo_material3(item){
  if(item.value.slice(0,8) == "Adhesivo"){
    document.getElementById('troqueladoadh2').style.display = "initial";
    document.getElementById('troquelado2').style.display = "none";
    document.getElementById('troqueladoadh2').required = true;
    document.getElementById('troquelado2').required = false;
    document.getElementById('troquelado2').value = "";
    document.getElementById("impresionr2").value = "Sin impresion";
    document.getElementById("impresionr2").disabled = true;

  }else{
    document.getElementById('troqueladoadh2').style.display = "none";
    document.getElementById('troquelado2').style.display = "initial";
    document.getElementById('troquelado2').required = true;
    document.getElementById('troqueladoadh2').required = false;
    document.getElementById('troqueladoadh2').value = "";

    document.getElementById("impresionr2").disabled = false;
  }
}

function chequeo_material4(item){
  if(item.value.slice(0,8) == "Adhesivo"){
    document.getElementById('troqueladoadh3').style.display = "initial";
    document.getElementById('troquelado3').style.display = "none";
    document.getElementById('troqueladoadh3').required = true;
    document.getElementById('troquelado3').required = false;
    document.getElementById('troquelado3').value = "";
    document.getElementById("impresionr3").value = "Sin impresion";
    document.getElementById("impresionr3").disabled = true;

  }else{
    document.getElementById('troqueladoadh3').style.display = "none";
    document.getElementById('troquelado3').style.display = "initial";
    document.getElementById('troquelado3').required = true;
    document.getElementById('troqueladoadh3').required = false;
    document.getElementById('troqueladoadh3').value = "";

    document.getElementById("impresionr3").disabled = false;
  }
}

function chequeo_material5(item){
  if(item.value.slice(0,8) == "Adhesivo"){
    document.getElementById('troqueladoadh4').style.display = "initial";
    document.getElementById('troquelado4').style.display = "none";
    document.getElementById('troqueladoadh4').required = true;
    document.getElementById('troquelado4').required = false;
    document.getElementById('troquelado4').value = "";
    document.getElementById("impresionr4").value = "Sin impresion";
    document.getElementById("impresionr4").disabled = true;

  }else{
    document.getElementById('troqueladoadh4').style.display = "none";
    document.getElementById('troquelado4').style.display = "initial";
    document.getElementById('troquelado4').required = true;
    document.getElementById('troqueladoadh4').required = false;
    document.getElementById('troqueladoadh4').value = "";

    document.getElementById("impresionr4").disabled = false;
  }
}
// Regular map
function regular_map() {
var var_location = new google.maps.LatLng(-2.1545748, -79.9270623);

var var_mapoptions = {
center: var_location,
zoom: 17
};

var var_map = new google.maps.Map(document.getElementById("map-container"),
var_mapoptions);

var var_marker = new google.maps.Marker({
position: var_location,
map: var_map,
title: "Ingrafen"
});
}

// Initialize maps
google.maps.event.addDomListener(window, 'load', regular_map);

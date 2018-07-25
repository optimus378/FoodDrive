$(document).on('shown.bs.modal','#theModal', function () {
    initialize();
    disablecharacters();
    disablenumbers();
  })

$('body').on('click', '[data-toggle="modal"]', function(){
    $($(this).data("target")+' .modal-body').load($(this).data("remote"));
});  
var TableData = new Array();
$('#streetrows').on('click', 'input[type="button"]', function () {
    $(this).closest('tr').remove();
})
function submitForm(){
    $('#streetrows tr').each(function(row, tr){
      TableData[row]={
          "street": $(tr).find('td:eq(0)').text()
      }
    });
 var hidden = document.getElementById('streets')
 hidden.value = JSON.stringify(TableData)
 $('#form').submit();
 alert('success')
}
function initialize() {
    var input = document.getElementById('findStreet');
    var options={
      language: 'en-US',
      types:['geocode'],
      componentRestrictions:{country: 'us'}
      
    }
    new google.maps.places.Autocomplete(input, options);
  }
  
  google.maps.event.addDomListener(window, 'load', initialize);

function addStreet(){
var candidate = document.getElementById("findStreet");
fetch('/api/checkstreet/'+candidate.value)
.then(function(response){
  if (!response.ok){
    var getstreet = document.getElementById("findStreet");
    var table = document.getElementById("streetrows");
    var hidden = document.getElementById("streets")
    var count = document.getElementById("streettable").rows.length;
    var row = table.insertRow(0);
    var street = row.insertCell(0);
    var checkbox = row.insertCell(1);
    var roadname = findStreet.value.slice(0,-9)
    var tablerows=document.getElementsByTagName('td')
    street.innerHTML = roadname
    checkbox.innerHTML = '<input type="button" value="Delete"/>'
     }
  else{
    alert('Sorry, this street has already been claimed. ')
  }
})
}
function disablenumbers() {
  var $textarea = document.getElementById('findStreet');
  $textarea.addEventListener('input', function () {
     // $textarea.value = $textarea.value.replace(/[^\w\s]/gi, '');
      $textarea.value = $textarea.value
                                     .replace(/^[1-9]+$/i, '');

  });
}
function disablecharacters() {
  var $bags= document.getElementById('bags');
  $bags.addEventListener('input', function () {
     // $textarea.value = $textarea.value.replace(/[^\w\s]/gi, '');
      $bags.value = $bags.value
                                     .replace(/^[A-Z]+$/i, '');

  });
}
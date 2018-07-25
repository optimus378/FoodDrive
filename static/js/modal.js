function initialize() {
    var input = document.getElementById('findStreet');
    var options={
      language: 'en-US',
      types:['geocode'],
      componentRestrictions:{country: 'us'}
      
    }
    new google.maps.places.Autocomplete(input, options);
  }

 $(document).on('shown.bs.modal','#theModal', function () {
    initialize()
  })
  $('body').on('click', '[data-toggle="modal"]', function(){
    $($(this).data("target")+' .modal-body').load($(this).data("remote"));
});  
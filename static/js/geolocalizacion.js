function geoposicionar(direccion) {
        var mapCanvas = document.getElementById('map-canvas');
        var mapOptions = {
            zoom: 17,
            center: new google.maps.LatLng(4.0645573,-81.9853798)
        }        
        var mapa = new google.maps.Map(mapCanvas, mapOptions);
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode({'address': direccion}, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
              mapa.setCenter(results[0].geometry.location);
              var marker = new google.maps.Marker({
                map: mapa,
                position: results[0].geometry.location
              });
            } else {
              alert('Geocode was not successful for the following reason: ' + status);
            }
          });
    }

function geoposicionarVarios(locations) {
    var map = new google.maps.Map(document.getElementById('map-canvas'), {
      zoom: 10,
      center: new google.maps.LatLng(2.9854481,-73.0628792),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    
    var geocoder = new google.maps.Geocoder();

    var listado_nombre = [];

    for (var i = 0; i < locations.length; i++) {

        var nombre = locations[i][0];
        var infowin = new google.maps.InfoWindow({content: nombre})
        
        //var dir = locations[i][1];


        geocoder.geocode({'address': locations[i][1]}, function(results, status) {
                    
            if (status == google.maps.GeocoderStatus.OK) {

             
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    position: results[0].geometry.location,
                    map: map,
                    title: nombre,
                    info: nombre
                });                

                google.maps.event.addListener(marker, 'click', function() {
                    infowin.setContent(this.info);
                    infowin.open(map,this);
                  });
                }
            else
            {
                alert("some problem in geocode" + status);
            }
        }); 
    }}
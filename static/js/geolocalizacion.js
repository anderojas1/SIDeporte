function geoposicionar(direccion) {
        var mapCanvas = document.getElementById('map-canvas');
        var mapOptions = {
            zoom: 17,
            center: new google.maps.LatLng(3.4484337,-76.5368595)
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
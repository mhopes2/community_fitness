// MAPS
$maps = $('.block.maps .content .map_canvas');
console.log ($maps)
$maps.each(function(index, Element) {
    $infotext = $(Element).children('.infotext');
console.log("test")
    var myOptions = {
        'zoom': parseInt($infotext.children('.zoom').text()),
        'mapTypeId': google.maps.MapTypeId.ROADMAP
    };
    var map;
    var geocoder;
    var marker;
    var infowindow;
    var address = $infotext.children('.address').text() + ', '
            + $infotext.children('.city').text() + ', '
            + $infotext.children('.state').text() + ' '
            + $infotext.children('.zip').text() + ', '
            + $infotext.children('.country').text()
    ;
    var content = '<strong>' + $infotext.children('.location').text() + '</strong><br />'
            + $infotext.children('.address').text() + '<br />'
            + $infotext.children('.city').text() + ', '
            + $infotext.children('.state').text() + ' '
            + $infotext.children('.zip').text()
    ;
console.log(address)
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            myOptions.center = results[0].geometry.location;
            map = new google.maps.Map(Element, myOptions);
            marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location,
                title: $infotext.children('.location').text()
            });
            infowindow = new google.maps.InfoWindow({'content': content});
            google.maps.event.addListener(map, 'tilesloaded', function(event) {
                infowindow.open(map, marker);
            });
            google.maps.event.addListener(marker, 'click', function() {
                infowindow.open(map, marker);
            });
        } else {
            alert('The address could not be found for the following reason: ' + status);
        }
    });
});
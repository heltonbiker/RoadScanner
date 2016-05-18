#!/usr/bin/env python
# coding: utf-8

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>RoadScanner result</title>
    <meta charset="utf-8">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
        html { height: 100% }
        body { height: 100%; margin: 0; padding: 0 }
        #map_canvas { height: 100%; width: 100% }
    </style>

    <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
        
    <script type="text/javascript">

        var bounds = new google.maps.LatLngBounds();

        function addRoad(road, map) {
            var coordinates = [];
            for (var i = 0; i < road.length; i++) {
                var ll = road[i];
                gll = new google.maps.LatLng(ll[1], ll[0])
                coordinates.push(gll);
                bounds.extend(gll)
            }            
            var percurso = new google.maps.Polyline({path: coordinates, strokeColor: "red"});
            percurso.setMap(map);
        }

        function initialize () {
            
            var mapOptions = {
                center: new google.maps.LatLng(-30.212202,-51.362572),
                zoom: 11,
                mapTypeId: google.maps.MapTypeId.HYBRID
            };
            var map = new google.maps.Map(document.getElementById("map_canvas"),
                mapOptions);
            
            roads = $$$$
            
            for (var i = 0; i < roads.length; i++) {
                addRoad(roads[i], map);
            }

            map.fitBounds(bounds);
        }
            
        google.maps.event.addDomListener(window, 'load', initialize);
            
    </script>
</head>

<body>
    <div id="map_canvas"></div>

</body>
</html>"""

def createMap(paths, fname):
    source = template.replace("$$$$", str(paths))
    with open(fname, 'w') as out:
        out.write(source)
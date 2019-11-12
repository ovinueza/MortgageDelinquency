// Store our API endpoint inside queryUrl
var link ="static/data/unitedstates.geojson";

var map = L.map("map", {
  center: [37.09, -95.75],
  zoom: 4
});

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: API_KEY
}).addTo(map);



// Function that will determine the color of a State based on the NumberOfForeclosures
function chooseColor(NFORECLOSURES) {
  if (NFORECLOSURES <= 0) {
      return "#001173";
  } else if (NFORECLOSURES <= 10) {
      return "#fff7d9";
  }else if (NFORECLOSURES <= 20) {
      return "#FFEDA0";
  } else if (NFORECLOSURES <= 30) {
      return "#FED976";
  } else if (NFORECLOSURES <= 40) {
      return "#ffd700";
  } else if (NFORECLOSURES <= 50) {
      return "#FEB24C";
  } else if (NFORECLOSURES <= 60) {
      return "#FFA500";
  } else if (NFORECLOSURES <= 70) {
      return "#fd8d3c";
  } else if (NFORECLOSURES <= 80) {
      return "#FC4E2A";
  } else if (NFORECLOSURES <= 90) {
    return "#E31A1C";
  } else if (NFORECLOSURES <= 100) {
      return "#BD0026";
  } else {
      return "#8b0000";
  };
}

// Grabbing our GeoJSON data..
d3.json(link, function(data) {
  // Creating a geoJSON layer with the retrieved data
 //State lines layer

  //county layer
  L.geoJson(data, {
    // Style each feature (in this case Number Of Foreclosures)
    style: function(feature) {
      console.log(data);
      return {
        color: "black",
        // Call the chooseColor function to decide which color to color our Number Of Foreclosures (color based on CNTYNAME)
        fillColor: chooseColor(feature.properties.NFORECLOSURES),
        fillOpacity: 0.4,
        weight: 1 
      };
    },


    // Called on each feature
    onEachFeature: function(feature, layer) {
      // Set mouse events to change map styling
      layer.on({
        // When a user's mouse touches a map feature, the mouseover event calls this function, that feature's opacity changes to 90% so that it stands out
        mouseover: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.7
          });
        },
        // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to 50%
        mouseout: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.4
          });
        },
        // When a feature (NumberOfForeclosures) is clicked, it is enlarged to fit the screen
        click: function(event) {
          map.fitBounds(event.target.getBounds());
        }
      });
      // Giving each feature a pop-up with information pertinent to it
      layer.bindPopup("<h3> Avg Rate: " + feature.properties.AVGINTERESTRATE +", " + feature.properties.STATE+"</h3>"
      + "<hr>" +"<h3> Foreclosures: " + feature.properties.NFORECLOSURES + "</h3>");
    
  
    }

  }).addTo(map);

});
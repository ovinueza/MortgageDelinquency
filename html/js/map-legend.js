
  function getColor(NFORECLOSURES) {
    return NFORECLOSURES> 100 ? "#8b0000":
    NFORECLOSURES>90?"#BD0026":
    NFORECLOSURES>80?"#E31A1C":
    NFORECLOSURES>70? "#FC4E2A":
    NFORECLOSURES>60? "#fd8d3c":
    NFORECLOSURES>50? "#FFA500":
    NFORECLOSURES>40? "#FEB24C":
    NFORECLOSURES>30? "#ffd700":
    NFORECLOSURES>20? "#FED976":
    NFORECLOSURES>10? "#FFEDA0":
    NFORECLOSURES>0? "#fff7d9":
    NFORECLOSURES>-1? "#00FFFFFF":
    "#00FFFFFF"
  };


 var legend = L.control({ position: "bottomright" });
 legend.onAdd = function() {
   var div = L.DomUtil.create("div", "info legend");
   NFORECLOSURES= [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
   labels=[];
 //Loop NFORECLOSURES values
 for (var i = 0; i < NFORECLOSURES.length; i++) {
   div.innerHTML += '<i style="background:' + getColor(NFORECLOSURES[i] + 1) + '"></i> ' 
   + NFORECLOSURES[i] + (NFORECLOSURES[i + 1] ? '&ndash;' + NFORECLOSURES[i + 1] + '<br>' : '+');
   };
   return div;

};

 legend.addTo(map);

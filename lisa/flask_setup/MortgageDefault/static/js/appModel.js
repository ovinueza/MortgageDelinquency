
//builds plots of regression analysis
function hazardChart(state) {
  var urlHaz = "/model/hazard/"+state;
  d3.json(urlHaz).then(function(haz_result) {
 
    var age = haz_result.age;
    console.log("hazard chart: "+age)
    var int_rate = haz_result.int_rate;
    var fit_string_short = `L = ${haz_result.test_int.toFixed(2)} + ${haz_result.test_slope.toFixed(2)}*VC`;
    var test_fit = haz_result.test_fit;
    var int_rate = haz_result.int_rate;

    // life expectancy regression fit plot
    var trace = { 
      x: age,
      y: int_rate,    
      mode: "markers",
      name: "age"
      }
    var trace_fit = { 
      x: age,
      y: test_fit,
      mode: "lines",
      name: fit_string_short 

    }
    testPlot = [trace,trace_fit];
    var layout = {
      title: "Nonsense Linear Regression Fit",
      xaxis: {title:"Data 1"},
      yaxis: {title:"Data 2"}
    }
    Plotly.newPlot("testRegression",testPlot,layout);
    
 
  });
} 

function init() {
  // Grab a reference to the dropdown select element
  var selectorState = d3.select("#selState");
  // Use the list of vaccine names to populate the select options
  d3.json("/states").then((states) => {
    states.forEach((PropertyState) => {
      selectorState
        .append("option")       
        .text(PropertyState)
        .property("value", PropertyState);
    });
    // // Use the first country/vaccine from the list to build the initial plots
    const firstState = states[0];
    currentState = firstState;
 
  hazardChart(currentState);
});
}

function stateChanged(newState) {
//   // Fetch new data each time a new sample is selected 
  currentState = newState;
  console.log("Function stateChanged, newState: "+newState)
  regressionChart(currentState);
}

var currentState = "";
// Initialize the dashboard
init();



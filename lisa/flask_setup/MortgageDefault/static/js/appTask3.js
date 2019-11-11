
//builds plots of regression analysis
function regressionChart(vaccine, country) {
  var urlReg = "/regression/infantmortality/"+vaccine+"/"+country;
  d3.json(urlReg).then(function(reg_result) {
    var vax_cov = reg_result.vax_cov;
    var inf_mort = reg_result.int_mort;
    var fit_string_inf = `Infant Mortality = ${reg_result.inf_int} + ${reg_result.inf_slope}*Vaccination Coverage`;
    var fit_string_inf_short = `I = ${reg_result.inf_int.toFixed(2)} + ${reg_result.inf_slope.toFixed(2)}*VC`;
    var inf_fit = reg_result.inf_fit;
    var inf_mort = reg_result.inf_mort;
    var inf_resid = reg_result.inf_resid;

    // Infant mortality regression fit plot
    var trace_inf = { 
      x: vax_cov,
      y: inf_mort,
      mode: "markers",
      name: "Observed Infant Mortality"    
    }
    var trace_inf_fit = { 
    x: vax_cov,
    y: inf_fit,
    mode: "lines",
    name: fit_string_inf_short    
    }

    infVaxPlot = [trace_inf,trace_inf_fit];
    var layout_inf = {
      title:"Infant Mortality Linear Regression Fit",
      xaxis: {title:"Vaccination Coverage"},
      yaxis: {title:"Infant Mortality"}
    }
    
    Plotly.newPlot("infRegression",infVaxPlot,layout_inf);

    //infant mortality residual plot 
    var trace_inf_resid = { 
      x: inf_resid,
      y: inf_fit,    
      mode: "markers"
      }
    infResidPlot = [trace_inf_resid];
    var layout_infResid = {
      title:"Infant Mortality Residual Plot",
      xaxis: {title:"Residuals(Observed -Predicted) "},
      yaxis: {title:"Predicted Infant Mortality"}
    }
    Plotly.newPlot("infResid",infResidPlot,layout_infResid);

        // inf qq plot
        var trace_inf_qq = { 
          x: reg_result.osm_qq_inf,
          y: reg_result.osr_qq_inf,    
          mode: "markers",
          name: "Quantiles"
          }
        var trace_inf_fit_qq = { 
          x: reg_result.osm_qq_inf,
          y: reg_result.qq_fit_inf,
          mode: "lines", 
          name: "Least Squares Fit"
        }
        infQQPlot = [trace_inf_qq,trace_inf_fit_qq];
        var layout_inf_qq = {
          title: "Infant Mortality Normal Q-Q Plot",
          xaxis: {title:"Theoretical Quantiles"},
          yaxis: {title:"Sample Quantiles"}
        }
        Plotly.newPlot("infQQ",infQQPlot,layout_inf_qq);

});
  
} 

function init() {
  // Grab a reference to the dropdown select element
  var selectorVaccine = d3.select("#selVaccine");
  // Use the list of vaccine names to populate the select options
  d3.json("/vaccine_names").then((vaccines) => {
    vaccines.forEach((Vaccine) => {
      selectorVaccine
        .append("option")       
        .text(Vaccine)
        .property("value", Vaccine);
    });
    // // Use the first country/vaccine from the list to build the initial plots
    const firstVax = vaccines[0];
    currentVax = firstVax;
  
  var selectorCountry = d3.select("#selCountry");

  // Use the list of countries to populate the select options
  d3.json("/countries").then((countries) => {
    countries.forEach((Country) => {
      selectorCountry
        .append("option")       
        .property("value", Country)
        .text(Country);
    });
    // // Use the first sample from the list to build the initial plots
    const firstCountry = countries[0]; 
    currentCountry = firstCountry;
  regressionChart(currentVax, currentCountry);
});
});
}

function vaxChanged(newVax) {
//   // Fetch new data each time a new sample is selected 
  currentVax = newVax;
  console.log("Function vaxChanged, newVax: "+newVax)
  regressionChart(currentVax, currentCountry);
}

function countryChanged(newCountry){
  console.log("Function countryChanged, newCountry: "+newCountry)
  currentCountry = newCountry;
  regressionChart(currentVax, currentCountry);
}

var currentCountry = "";
var currentVax = "";
// Initialize the dashboard
init();



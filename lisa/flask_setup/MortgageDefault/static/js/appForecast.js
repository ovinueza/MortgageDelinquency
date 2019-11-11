
//build charts for trends over time plots
function buildCharts(vax, country) {
  //url for the sample
  var urlVax = "/metadata/"+vax +"/"+country;
  var urlLife= "/countrydata/"+country;
  // console.log("buildCharts, vax:" +vax+"country:" +country);
  // console.log("URL: "+url);
  d3.json(urlVax).then(function(selection) {
    var year = [];
    var coverage = [];
     for (i = 0; i < selection.length;i++) {
       year.push(selection[i].Year);
       coverage.push(selection[i].Coverage);
    }

    traceVax = {
      x: year,
      y: coverage
    }
    vaxPlot = [traceVax];
    var layout = {
      title: "Vaccination Coverage",
      xaxis: {title:"Year"},
      yaxis: {title:"Coverage"}
    }
    Plotly.newPlot("vaxChart",vaxPlot,layout);
  });

  d3.json(urlLife).then(function(selection) {
    var year = [];
    var lifeExp = [];
    var infMort = [];
     for (i = 0; i < selection.length;i++) {
       year.push(selection[i].Year);
       lifeExp.push(parseFloat(selection[i].Life_Expectancy));
       infMort.push(parseFloat(selection[i].Infant_Mortality));
    }
    // console.log("buildCharts, urlLife, infMort: "+infMort);
    // console.log("buildCharts, urlLife, lifeExp: "+lifeExp);
    // console.log("buildCharts, urlLife, selection.Life:"+selection.Life_Expectancy)
    traceLife = {
      x: year,
      y: lifeExp,
      name: "Life Expectancy"
    }
    traceInf = {
      x: year,
      y:infMort,
      yaxis: 'y2',
      name: "Infant Mortality"
    }
    lifePlot = [traceLife,traceInf];
    var layout = {
      title: "Life Expectancy and Infant Mortality",
      margin: {
        l: 50, r: 100, b: 50, t: 50, pad: 2
      },
      xaxis: {title:"Year"},
      yaxis: {title:"Life Expectancy"},
      yaxis2: {
        title:"Infant Mortality",
        overlaying: 'y',
        side: 'right'}
      }
    Plotly.newPlot("lifeChart",lifePlot,layout);
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
    // console.log("First Country ", firstCountry);
    currentCountry = firstCountry;
    // console.log("inside current country "+currentCountry)
  buildCharts(currentVax, currentCountry);
  // regressionChart(currentVax, currentCountry);
});
});
}

function vaxChanged(newVax) {
//   // Fetch new data each time a new sample is selected 
  currentVax = newVax;
  console.log("Function vaxChanged, newVax: "+newVax)
  buildCharts(newVax, currentCountry);
  // regressionChart(currentVax, currentCountry);
}

function countryChanged(newCountry){
  console.log("Function countryChanged, newCountry: "+newCountry)
  currentCountry = newCountry;
  buildCharts(currentVax, newCountry);
  // regressionChart(currentVax, currentCountry);
}

var currentCountry = "";
var currentVax = "";
// Initialize the dashboard
init();



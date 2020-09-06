//Code runs through the counties demographic csv file and creates a JSON file
//with FIPS, name, state, and POP_ESTIMATE_2018 as the fields 

const csv = require('csv-parser');
const fs = require('fs');


var array = new Array();

let jsonData;
fs.createReadStream('./data/csv/counties.csv')
  .pipe(csv())
  .on('data', (row) => {
    var county = new Object();
    county.FIPS = row["FIPS"]
    county.name = row["Area_Name"]; 
    county.state = row["State"];
    county.POP_ESTIMATE_2018 = row["POP_ESTIMATE_2018"];
    array.push(county);
  
  })
  .on('end', () => {
    console.log(array);
    jsonData = JSON.stringify(array, '\t', 2); 
    fs.writeFile("./data/countyDemographics.json", jsonData, function(err){
      if(err){
        console.log(err);
      }

    });
    
    console.log('CSV file successfully processed');
  });


console.log(array);

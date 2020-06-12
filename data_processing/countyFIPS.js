//Code runs through the counties demographic csv file and creates a JSON file
//with FIPS, name, state, and POP_ESTIMATE_2018 as the fields 

const csv = require('csv-parser');
const fs = require('fs');
var count = 0;

console.log("Hello World");
fs.createReadStream('./data/csv/deaths_timeseries.csv')
  .pipe(csv())
  .on('data', (row) => {
    let fips;
    fips = row["FIPS"] +':countySchema, ';
    count++;
    if(count >= 8){
        count = 0;
        fips = fips + '\n'
    }
    fs.appendFile("./data/fips.txt", fips, function(err){
      if(err){
        console.log(err);
      }

    });
  
  })
  .on('end', () => {
    console.log('CSV file successfully processed');
  });

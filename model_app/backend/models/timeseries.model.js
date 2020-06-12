const mongoose = require("mongoose");
var lineReader = require('line-reader');


// embedded county schema
const countySchema = mongoose.Schema({
  infected:{
    type:Number, 
    required: true,
  },
  CKey:{
    type:String,
    required:true,
  },
  death:{
    type:Number,
    required:true
  },
  ">50 gatherings":{
    type: Boolean
  },
  ">500 gatherings":{
    type:Boolean
  },
  "public schools":{
    type:Boolean
  },
  "restaurant dine-in":{
    type:Boolean  },
  "entertainment/gym":{
    type:Boolean
  },
  "federal guidelines":{
    type:Boolean
  },
  "foreign travel ban:":{
    type:Boolean
  }
});

// Date schema
// TODO: fill in county fips as keys?
const schema = mongoose.Schema({
  date: Date,
}, {strict: false});


var reader = require('line-reader');

reader.eachLine('fips.txt', function(line, last) {
  console.log("Line"+line);
  var fips = line;
  schema.add({fips:countySchema});

});
module.exports = mongoose.model("Timeseries", schema);
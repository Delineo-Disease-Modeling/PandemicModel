const mongoose = require("mongoose");

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
  1001: countySchema
}, {strict: false});

module.exports = mongoose.model("Timeseries", schema);
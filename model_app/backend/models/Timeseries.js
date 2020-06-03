const mongoose = require("mongoose");

// TODO: fill in actual schema
const schema = mongoose.Schema({
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
    type: Boolean,
    required:true
  },
  ">500 gatherings":{
    type:Boolean,
    required:true,
  },
  "public schools":{
    type:Boolean,
    required:true,
  },
  "restaurant dine-in":{
    type:Boolean,
    required:true
  },
  "entertainment/gym":{
    type:Boolean,
    required:true,
  },
  "federal guidelines":{
    type:Boolean,
    required:true,
  },
  "foreign travel ban:":{
    type:Boolean,
    required:true,
  }
});

module.exports = mongoose.model("Timeseries", schema);
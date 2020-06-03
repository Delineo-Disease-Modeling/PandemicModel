const mongoose = require("mongoose");
const Schema = mongoose.Schema;

// TODO: fill in actual schema
const demographicSchema = new Schema({
  FIPS: {type: Number},
  State: {type: String},
  Area_Name: {type: String},
  POP_ESTIMATE_2018: {type: Number}
});

//Consider const protecting later
module.exports = mongoose.model("Demographics", demographicSchema);
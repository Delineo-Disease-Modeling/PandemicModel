const mongoose = require("mongoose");
const Schema = mongoose.Schema;

// Simple schema with fields for the county's name, 
// the state it's in, and the population
const demographicSchema = new Schema({
	FIPS: {type: Number, required: true},
	State: {type: String, required: true},
	Area_Name: {type: String, required: true},
	POP_ESTIMATE_2018: {type: Number, required: true}
}, {strict: false});

// Example object for what to return
const demographicObj = {
	FIPS: 1,
	State: 1,
	Area_Name: 1,
	POP_ESTIMATE_2018: 1
}

//Consider const protecting later
module.exports = mongoose.model("Demographics", demographicSchema)
module.exports.demographicObj = demographicObj
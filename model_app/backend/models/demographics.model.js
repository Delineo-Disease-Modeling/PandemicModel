// Dependencies
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

// Simple schema with fields for the county's name, FIPS code, the state it's in, and its population
// The {strict: false} option allows for additional fields to exist in schema instances
const demographicSchema = new Schema({
	FIPS: {type: Number, required: true},
	State: {type: String, required: true},
	Area_Name: {type: String, required: true},
	POP_ESTIMATE_2018: {type: Number, required: true}
}, {strict: false});

// Example object for what to return in a query
// We only select these four fields, plus the ObjectID
const demographicObj = {
	FIPS: 1,
	State: 1,
	Area_Name: 1,
	POP_ESTIMATE_2018: 1
};

// Export schema and example object
module.exports = mongoose.model("Demographics", demographicSchema);
module.exports.demographicObj = demographicObj;
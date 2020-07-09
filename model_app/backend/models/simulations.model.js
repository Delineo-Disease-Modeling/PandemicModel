// Dependencies
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

// Simulation schema: fields for job status, and results when job is complete
const simulationSchema = new Schema({
//	Status: {type: String, required: true},
	Results: Object
});

// Export schema
module.exports = mongoose.model("Simulations", simulationSchema);
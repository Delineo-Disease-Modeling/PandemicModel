// Dependencies
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

// Simulation schema: fields for job status, and results when job is complete
// tbh job status probably isn't necessary now bc i set up an event listener for the jobId, but I kept it
// there just bc it's easier to visually see in the db when it changes from incomplete to complete
const simulationSchema = new Schema({
	Status: {type: String, required: true},
	Results: Object
});

// Export schema
module.exports = mongoose.model("Simulations", simulationSchema);
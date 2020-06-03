const mongoose = require('mongoose');
const Schema = mongoose.Schema;

/**
 * Simple schema which has fields for the county's name, 
 * the state it's in, and the population.
 */
const countySchema = new Schema({
    name: {type: String, required: true},
    state: {type: String, required: true},
    population: {type: Number, required: true}
});

const County = mongoose.model('County', countySchema);
module.exports = County;
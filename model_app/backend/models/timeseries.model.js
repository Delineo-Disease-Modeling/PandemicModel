const mongoose = require("mongoose");

// TODO: fill in actual schema
const schema = mongoose.Schema({
  Date: Date
});

module.exports = mongoose.model("Timeseries", schema);
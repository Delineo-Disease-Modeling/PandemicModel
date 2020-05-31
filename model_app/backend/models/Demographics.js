const mongoose = require("mongoose");

// TODO: fill in actual schema
const schema = mongoose.Schema({
  FIPS: Number
});

module.exports = mongoose.model("Demographics", schema);
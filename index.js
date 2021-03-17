// index.js file
// run "npm install" then use "node index.js" to run locally
const express = require("express");
const app = express();
const port = 5000;
const data = require('./Simulation/submodules.json');

app.get("/", (req, res) => {
  res.send(data);
});

app.listen(port, () => {
  console.log(`Express app listening at http://localhost:${port}`);
});

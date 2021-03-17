// index.js file
const express = require("express");
const app = express();
const port = 5000;

app.get("/", (req, res) => {
  res.send("Testing Express!");
});

app.listen(port, () => {
  console.log(`Express app listening at http://localhost:${port}`);
});

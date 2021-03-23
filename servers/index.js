const express = require("express");
const server1 = express();
const jsonData = require("../package.json");

// sends post request to itself, then read by other server
server1.post("/test", (req, res) => {
  const { spawn } = require("child_process");
  const pyProg = spawn("python3", ["test.py"]);
  pyProg.stdout.on("data", function (data) {
    console.log(data.toString());
    res.write(data); // send python file
    res.end("end");
  });
  res.json(jsonData); // send JSON file
  console.log(jsonData.toString());
  // console.log(`Query String: ${req.query}`);
  // console.log(`Body: ${req.body}`);
});

// listen on port 4000
server1.listen(4000, () => console.log("Application listening on port 4000!"));

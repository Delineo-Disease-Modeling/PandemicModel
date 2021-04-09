const express = require("express");
const simulator = express();
const jsonData = require("./data.json");
const http = require("http");
const fs = require("fs");

simulator.use(express.json());

// returns post request to website then read by other server
simulator.post("/simulator", (req, res) => {
  console.log(req.body);
  const { spawn } = require("child_process");
  const pyProg = spawn("python3", ["../simulation/master", req.body]);
  pyProg.stdout.on("data", function (data) {
    console.log(data);
    res.write(data);
    res.end("end");
  });

  res.json(jsonData); // send new JSON file

  // read newly generated json file
  let data = ""; 
  fs.readFile("data.json", async (e, data) => {
    try {
      data = await JSON.parse(data);
      console.log(JSON.stringify(data));
    } catch (e) {
      throw e;
    }
  });

  // gets post request from other server
  var options = {
    host: "localhost",
    port: 3000,
    path: "/",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
  };
  // parses data from other server
  var httpreq = http.request(options, function (response) {
    response.setEncoding("utf8");
    response.on("data", function (chunk) {
      console.log("body: " + chunk);
    });
    response.on("end", function () {
      res.json(JSON.stringify(jsonData));
    });
  });

  // handle error on failed POST
  httpreq.on("error", (e) => {
    console.error(`problem with request: ${e.message}`);
  });

  httpreq.write(data);
  httpreq.end();
});

// listen on port 22
simulator.listen(22, () =>
  console.log("Application listening on port 22!")
);

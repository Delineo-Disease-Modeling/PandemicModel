const express = require("express");
const simulator = express();
const jsonData = require("../package.json");
const http = require("http");
const fs = require("fs");

// returns post request to website then read by other server
simulator.post("/test", (req, res) => {
  const { spawn } = require("child_process");
  const pyProg = spawn("python3", ["test.py"]);
  pyProg.stdout.on("data", function (data) {
    console.log(data.toString());
    res.write(data); // send python file
    res.end("end");
  });
  res.json(jsonData); // send JSON file
  console.log(jsonData.toString());

  let data = "";
  fs.readFile("data.json", async (e, data) => {
    try {
      data = await this.data;
      console.log(data);
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
      "Content-Type": "application/x-www-form-urlencoded",
      "Content-Length": Buffer.byteLength(data),
    },
  };
  // parses data from other server
  var httpreq = http.request(options, function (response) {
    response.setEncoding("utf8");
    response.on("data", function (chunk) {
      console.log("body: " + chunk);
    });
    response.on("end", function () {
      res.send("Simulator sent POST to Website");
    });
  });
  httpreq.write(data);
  httpreq.end();
});

// listen on port 4000
simulator.listen(4000, () =>
  console.log("Application listening on port 4000!")
);

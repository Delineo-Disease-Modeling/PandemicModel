const express = require("express");
const simulator = express();
const https = require("https");
const port = 22; // process.env.PORT || 
// const jsonData = require("./data.json");
// const fs = require("fs");

var privateKey  = fs.readFileSync('/etc/pki/tls/certs/covidmod.isi.jhu.edu.2021.cer', 'utf8');
var certificate = fs.readFileSync('/etc/pki/tls/private/covidmod.isi.jhu.edu.key', 'utf8');
var credentials = {key: privateKey, cert: certificate};
var httpsServer = https.createServer(credentials, app);

simulator.use(express.json());

// returns post request to website then read by other server
simulator.post("/", (req, res) => {
  let data = "";
  console.log(req.body);
  const { spawn } = require("child_process");
  const pyProg = spawn("python3", ["../simulation/master.py"]);
  pyProg.stdout.on("data", function (data) {
    this.data = data;
    console.log(data);
    if (data == "") { 
      console.log("returned invalid json");
    }
    res.write(data);
    res.end("end");
  });

  // gets post request from other server
  var options = {
    host: "covidweb.isi.jhu.edu",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
  };
  // parses data from other server
  var httpsreq = https.request(options, function (response) {
    response.setEncoding("utf8");
    response.on("data", function (chunk) {
      console.log("body: " + chunk);
    });
    response.on("end", function () {
      res.json(data); //JSON.stringify(data));
    });
  });

  // handle error on failed POST
  httpsreq.on("error", (e) => {
    console.error(`problem with request: ${e.message}`);
  });

  httpsreq.write(data);
  httpsreq.end();
});

// listen on port 443
httpsServer.listen(port, () =>
  console.log(`Application listening on port ${port}!`)
);

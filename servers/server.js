const express = require("express");
const server1 = express();
const querystring = require("querystring");
const http = require("http");
const port = process.env.PORT || 3000;
// server1 = unityGame, server2 = simulator
server1.get("/", function (req, res) {
  var data = querystring.stringify({
    username: "myname",
    password: "pass",
  });
  // gets post request from other server
  var options = {
    host: "localhost",
    port: 4000,
    path: "/test",
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
      res.send("ok");
    });
  });
  httpreq.write(data);
  httpreq.end();
});

// listen on port 3000(or whichever port is open)
server1.listen(port, () => console.log(`Listening on ${port}`));
/*
  Unity server -> makes request to simulator (passes user data json)
  then simulator passes back json (different file, visual version of data) 
  to unity game to start game.

  testing: python -> outputs json to a file
  get json data file then return it (response, perhaps 
    listen for post/get request)
*/

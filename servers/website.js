const express = require("express");
const website = express();
const querystring = require("querystring");
const http = require("http");
const port = process.env.PORT || 3000;

// website.set("view engine", "ejs");

website.get("/", function (req, res) {
  // res.render("index");
  // document.getElementById("btn").addEventListener("click", postReq);
  // function postReq() {
    let data = querystring.stringify({
      username: "myname",
      password: "pass",
    });
    // gets post request from other server
    let options = {
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
    let httpreq = http.request(options, function (response) {
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
  // }
});

website.post("/", (req, res) => {
  res.write("Test"); // display
  console.log("Test");
  console.log(`Query String: ${req.query}`);
  console.log(`Body: ${req.body}`);
});

// listen on port 3000(or whichever port is open)
website.listen(port, () => console.log(`Listening on ${port}`));

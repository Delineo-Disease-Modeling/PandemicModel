const express = require("express");
const website = express();
const querystring = require("querystring");
const http = require("http");
const port = process.env.PORT || 3000;
const data = require("../package.json");

website.use(express.json());

// website.set("view engine", "ejs");

website.get("/", function (req, res) {
  // res.render("index");
  // document.getElementById("btn").addEventListener("click", postReq);
  // function postReq() {
  // let data = querystring.stringify({
  //   username: "myname",
  //   password: "pass",
  // });
  // gets post request from other server
  let options = {
    host: "localhost",
    port: 4000,
    path: "/test",
    method: "POST",
    headers: {
      //application/x-www-form-urlencoded
      "Content-Type": "application/json"
    },
  };
  // parses data from other server
  let httpreq = http.request(options, function (response) {
    response.setEncoding("utf8");
    response.on("data", function (chunk) {
      console.log("body: " + chunk);
    });
    response.on("end", function () {
      res.send("Website sent POST to Simulator");
    });
  });
  httpreq.write(JSON.stringify(data));
  // httpreq.write(data);
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

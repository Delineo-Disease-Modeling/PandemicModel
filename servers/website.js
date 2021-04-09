const express = require("express");
const website = express();
// const querystring = require("querystring");
const http = require("http");
const port = 80 || process.env.PORT;
const postData = require("../package.json");

website.use(express.json());

website.get("/", function (req, res) {
  let data = JSON.stringify(postData); // stringify initial json data

  // sends POST request from other server
  let options = {
    host: "covidmod.local",
    path: "/",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
  };

  // organizes data to be sent to simulator
  let httpreq = http.request(options, function (response) {
    response.setEncoding("utf8");
    response.on("data", function (chunk) {
      console.log("body: " + chunk);
    });
    response.on("end", function () {
      res.json(data); // shows data being sent to covidmod.local
    });
  });

  // handle error on failed POST
  httpreq.on("error", (e) => {
    console.error(`problem with request: ${e.message}`);
  });

  httpreq.write(data);
  httpreq.end();
});

website.post("/", (req, res) => {
  console.log("New JSON passed in return");
  // console.log(`Query String: ${req.query}`);
  console.log(`Body: ${req.body}`);
});

// listen on port 80
website.listen(port, () => console.log(`Listening on ${port}`));

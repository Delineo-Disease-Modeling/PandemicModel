// dependencies
const mongoose = require('mongoose')
const express = require('express')
//const morgan = require('morgan')
//const errorhandler = require('errorhandler')
//const bodyParser = require('body-parser') //I think Express versions >= 4.16.0 have this built in
const routes = require("./routes")
const cors = require('cors')
const app = express()
const port = process.env.PORT || 5000; //Node.js uses port 5000 for dev server

require('dotenv').config(); //Allows us to use environment variables from .env file
const uri = process.env.ATLAS_URI;

//app.use(morgan('dev'))
//app.use(errorhandler())
app.use(cors())
app.use(express.json()) //Let's us parse JSON since server that's server format
//app.use('/demographics', routes.dem)
//app.use('/timeseries', routes.time)

mongoose.connect(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

/**
 * Let's us know if we connected to MongoDB database
 */
const connection = mongoose.connection;
connection.once('open', () => {
  console.log("MongoDB database connection established successfully");
})

const demographicsRouter = require('./routes/demographics');
const countiesRouter = require('./routes/counties');

app.use('/demographics', demographicsRouter);
app.use('/counties', countiesRouter);

/**
 * Should be listening to port 5000, will tell us if not
 */
app.listen(port, () => {
  console.log(`Development server is running on port: ${port}`);
});
/**
 * Dependencies
 * mongoose: A mongoDB object modelling library that allows us to manage data 
 * relationships, provide schema validation, and translate between code objects 
 * and representations of those objects in mongoDB.
 * 
 * express: A Node.js web application server framework.
 * 
 * cors: Cross-Origin Resource Sharing. Protocol that allows scripts running on 
 * browser clinet to interact with resources from a different origin.
 */
const mongoose = require('mongoose')
const express = require('express')
const cors = require('cors')
const app = express()
const port = process.env.PORT || 5000; //Node.js uses port 5000 for development server

require('dotenv').config(); //Allows us to use environment variables from .env file
const uri = process.env.ATLAS_URI;

app.use(cors())
app.use(express.json()) //Let's us parse JSON since server that's server format

mongoose.connect(uri, {
  useNewUrlParser: true, //Fall back to old MongoDB connection string parser
  useUnifiedTopology: true //Opts in to MongoDB's new connection management engine
});

/**
 * Let's us know if we connected to MongoDB database
 */
const connection = mongoose.connection;
connection.once('open', () => {
  console.log("MongoDB database connection established successfully");
})

/**
 * Tell server where to look for demographics and timeseries routing instructions
 */
const router = require('./routes');
app.use('/demographics', router.dem);
app.use('/timeseries', router.time);
//app.use('/counties', router.county);

/**
 * Should be listening to port 5000, will tell us if not
 */
app.listen(port, () => {
  console.log(`Development server is running on port: ${port}`);
});
// dependencies
const mongoose = require('mongoose')
const express = require('express')
const morgan = require('morgan')
const errorhandler = require('errorhandler')
const bodyParser = require('body-parser')
const routes = require("./routes")

const app = express()
app.use(bodyParser.json())
app.use(morgan('dev'))
app.use(errorhandler())
app.use('/demographics', routes.dem)
app.use('/timeseries', routes.time)

// TODO: put this in env?
mongoose.connect('mongodb+srv://admin:covid19@covid19-g8npp.mongodb.net/test?retryWrites=true&w=majority', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})

app.listen(3000)
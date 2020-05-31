// dependencies
const app = require('express')
const Timeseries = require('../models/Timeseries')
const router = app.Router()

// middleware
router.param('dateId', (req, res, next, dateId) => {
	Timeseries.findOne({FIPS: dateId}, (error, id) => {
		if (error)
			return next(error)
		req.id = id
		next()	
	})
})

// read all
router.get('/', (req, res) => {
	Timeseries.find({}, null, {
			sort: {
				_id: -1
			}
		})
		.exec((error, results) => {
			if (error)
				return next(error)
			res.send(results)
		})
})

// read single date info
router.get('/:dateId', (req, res) => {
	res.send(req.id)
})

module.exports = router
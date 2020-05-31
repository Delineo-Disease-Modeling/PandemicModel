// dependencies
const app = require('express')
const Demographics = require('../models/Demographics')
const router = app.Router()

// middleware
router.param('countyId', (req, res, next, countyId) => {
	Demographics.findOne({FIPS: countyId}, (error, id) => {
		if (error)
			return next(error)
		req.id = id
		next()	
	})
})

// read all
router.get('/', (req, res) => {
	Demographics.find({}, null, {
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
router.get('/:countyId', (req, res) => {
	res.send(req.id)
})

module.exports = router
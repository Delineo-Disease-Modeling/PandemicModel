// dependencies
const app = require('express')
const Timeseries = require('../models/timeseries.model')
const router = app.Router()

// middleware
router.param('dateId', (req, res, next, dateId) => {
	Timeseries.findOne({date: new Date(dateId)}, (error, id) => {
		if (error)
			return next(error)
		req.id = id
		next()	
	})
})

// read all
router.get('/', (req, res) => {
	Timeseries.find({}).limit(10)
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

// CRUD - create
router.post('/', (req, res) => {
	// TODO: data validation and sanitization
	let newTimeseries = new Timeseries(req.body)
	newTimeseries.save()
		.then(() => res.json('Date Added'))
        .catch(err => res.status(400).json('Error: ' + err));
})

// CRUD - update
router.put('/:dateId', (req, res) => {
	if (req.body.date) 
		req.id.date = req.body.date
	// update embedded county schema here?
	req.id.save()
		.then(() => res.json('Date Updated'))
        .catch(err => res.status(400).json('Error: ' + err));
})

// CRUD - delete
router.delete('/:dateId', (req, res) => {
	req.id.remove((error, results) => {
		if (error)
			return next(error)
		res.send(results)
	})
})

module.exports = router
// dependencies
const Demographics = require('../models/demographics.model')
const router = require('express').Router()

// middleware
router.param('countyId', (req, res, next, countyId) => {
	Demographics.findOne({FIPS: countyId}, Demographics.demographicObj, (error, id) => {
		if (error)
			return next(error)
		req.id = id
		next()	
	})
})

/**
 * A get request will currently return all counties that have 
 * been posted to the database.
 */
router.get('/', (req, res) => {
	Demographics.find({}, Demographics.demographicObj)
		.then(county => res.json(county))
        .catch(err => res.status(400).json('Error: ' + err));
})

// read single county info
router.get('/:countyId', (req, res) => {
	demographic => res.json(demographic)
	res.send(req.id)
})

/**
 * Handles the posting of a new county into database.
 */
// I don't think we'll ever use this? I kept this here anyway though
// If we do use this, we should do some validation/sanitization of data
router.post((req, res) => {
	const fips = req.body.FIPS;
    const name = req.body.Area_Name;
    const state = req.body.State;
    const population = req.body.POP_ESTIMATE_2018;

    const newCounty = new Demographics({
    	fips,
        name,
        state,
        population,
    });

    newCounty.save()
        .then(() => res.json('County Added'))
        .catch(err => res.status(400).json('Error: ' + err));
});

module.exports = router;
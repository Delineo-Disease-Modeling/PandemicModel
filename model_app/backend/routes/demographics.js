// Dependencies
const Demographics = require('../models/demographics.model')
const router = require('express').Router()

// Middleware for state
// currently no error checking
router.param('stateId', (req, res, next, state) => {
	req.state = state;
	next();
})

// Middleware that finds a single county and saves it to req.id if :countyId is specified
router.param('countyId', (req, res, next, countyId) => {
	/* Querying by FIPS
	if (parseInt(countyId) instanceof Number) {
		Demographics.findOne({FIPS: countyId}, Demographics.demographicObj, (error, id) => {
			if (error)
				return next(error);
			else if (!id)
				return res.status(400).json('Error: Invalid FIPS code');
			req.id = id;
			next();
		})
	}
	*/
	// Syntax: Case sensitive, must enter county name with ' County'
	// Not really any error checking here either
	Demographics.findOne({Area_Name: countyId, State: req.state}, Demographics.demographicObj, (error, id) => {
		if (error)
			return next(error);
		else if (!id)
			return res.status(400).json('Error: Invalid County Name');
		req.id = id;
		next();
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

// Read single county info
router.get('/:stateId/:countyId', (req, res) => {
	demographic => res.json(demographic);
	res.send(req.id);
})

/**
 * Handles the update of a county into database. We'll probably never use this.
 */
 router.put('/:countyId', (req, res) => {
 	// error handling: at least one required field must exist in body request
 	// and if FIPS exists in body, it must match the database FIPS
 	if (!req.body.FIPS & !req.body.Area_Name & !req.body.State & !req.body.POP_ESTIMATE_2018)
 		return res.status(400).json('Error: Request body is invalid');
 	else if (req.body.FIPS & (req.id.FIPS != req.body.FIPS))
 		return res.status(400).json('Error: Mismatching FIPS code');

    if (req.body.Area_Name)
    	req.id.Area_Name = req.body.Area_Name;
    if (req.body.State)
    	req.id.State = req.body.State;
    if (req.body.POP_ESTIMATE_2018)
    	req.id.POP_ESTIMATE_2018 = req.body.POP_ESTIMATE_2018;
    
	req.id.save()
		.then(() => res.json('Date Updated'))
        .catch(err => res.status(400).json('Error: ' + err));
})

module.exports = router;
const router = require('express').Router();
let County = require('../models/counties.model');

/**
 * A get request will currently return all counties that have 
 * been posted to the database.
 */
router.route('/').get((req, res) => {
    County.find()
        .then(county => res.json(county))
        .catch(err => res.status(400).json('Error: ' + err));
});

/**
 * Handles the posting of a new county into database.
 */
router.route('/add').post((req, res) => {
    const name = req.body.name;
    const state = req.body.state;
    const population = req.body.population;

    const newCounty = new County({
        name,
        state,
        population,
    });

    newCounty.save()
        .then(() => res.json('County Added'))
        .catch(err => res.status(400).json('Error: ' + err));
});

module.exports = router;
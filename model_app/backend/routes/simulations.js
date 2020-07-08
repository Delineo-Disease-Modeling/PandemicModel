// Dependencies
const router = require('express').Router();
const Simulations = require('../models/simulations.model');
const {PythonShell} = require('python-shell');
const em = require('../events/emitter');

// middleware
router.param('id', (req, res, next, id) => {
	Simulations.findById(id, (error, obj) => {
		if (error) {
			return res.status(400).json(`Error: No simulation request with id ${id}`);
		}
		req.obj = obj;
	next();
	});
})

// No user input currently
// Extract user input from body, then run python scripts with user input as arguments
router.post('/', (req, res) => {
	let input = req.body;

	let options = {
		mode: 'text',
		scriptPath: process.env.SCRIPT_PATH,
		pythonPath: process.env.PYTHON_PATH,
		pythonOptions: ['-u'],
		//args: ['file.json']
	};

	// insert new simulation request in db, return MongoDB id or error
	let newSimulation = new Simulations({Status: "incomplete"})
	newSimulation.save()
		.then(results => {
			let jobId = results._id;
			res.status(200).send(jobId);

			// data exchange between node.js and python file
			// refer to: https://github.com/extrabacon/python-shell
			PythonShell.run('main.py', options, (err, results) => {
				if (err)
					throw err;
				// Results is an array consisting of messages collected during execution
				Simulations.findById(jobId, (error, id) => {
					if (error)
						throw error;
					id.Status = "complete";
					id.Results = results;
					id.save(e => {if (e) throw e;});
				});
				em.emit('finished');
				console.log('saved results to db');
			});
		})
		.catch(err => res.status(400).json('Error: ' + err));
})

// Get simulation results by id
router.get('/:id', (req, res) => {
	
	if (req.obj.Results) {
		res.send(req.obj.Results);
	}

	em.on('finished', () => {
		console.log('got here');
		// there's a small delay saving to db, so i temporarily hard coded a delay for 1.5 ms
		setTimeout(() => {
			Simulations.findById(req.obj._id, (error, obj) => {
				if (error)
					throw error;
				else if (obj.Results) {
					res.send(obj.Results);
				}
		})}, 1500);
	});
})

// Delete simulation results by id, returns deleted object
router.delete('/:id', (req, res) => {
	req.obj.remove((error, results) => {
		if (error)
			return next(error)
		res.send(results)
	})
})

module.exports = router
// Dependencies
const router = require('express').Router();
const {PythonShell} = require('python-shell');


// Extract user input from body, then run python scripts with user input as arguments
router.post('/', (req, res) => {
	let input = req.body;

	let options = {
		mode: 'text',
		scriptPath: '..\algo\test.py',
		args: [input]
	};

	// data exchange between node.js and python file
	// refer to: https://github.com/extrabacon/python-shell
	PythonShell.run('../algo/test.py', options, function (err, results) {
		if (err)
			throw err;
		// Results is an array consisting of messages collected during execution
		res.status(200).send(results);
	});
})

module.exports = router
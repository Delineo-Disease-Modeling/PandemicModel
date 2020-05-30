// script to convert csv file to json object

// description of correct usage
const usage = 'usage: node convertToJSON.js csvfilepath'

// dependencies
const fs = require('fs')
const path = require('path')
const csv = require('csvtojson')

// check for one command line argument
if (process.argv.length != 3) {
	console.error('Error: Expected CSV file path as argument')
	console.error(usage)
	process.exit(1)
}

// get path of a csv file, passed in as argument
const csvFilePath = process.argv[2]

// check that argument is a valid file
fs.lstat(csvFilePath, (err, stats) => {
	if (err || !stats.isFile()) {
		console.error('Error: Invalid file path')
		console.error(usage)
		process.exit(1)
	}
});

// parse csv file path
const parsedPath = path.parse(csvFilePath)

// check that file has correct CSV extension
if (!parsedPath.ext === '.csv') {
	console.error('Error: Must be a CSV file')
	console.error(usage)
	process.exit(1)
}

// what to name the file
const fileName = parsedPath.name

// Use csvtojson module
// parser parameters: keep periods in json headers, keep nulls, convert string to number
// csv file line hook: replace 'NA' with nulls
csv({
		flatKeys: true,
		nullObject: true,
		checkType: true
	}).fromFile(csvFilePath)
	// globally replace "NA" with null
	.preFileLine((fileLineString, lineIdx) => {
		return new Promise((resolve, reject) => {
			if (lineIdx > 0) {
				fileLineString = fileLineString.replace(/NA/g, null)
			}
			resolve(fileLineString);
		})
	})
	.then((jsonObj) => {
		// convert to json
		let data = JSON.stringify(jsonObj, null, 2)

		// async write json object to file
		fs.writeFile(path.join(__dirname, 'data', fileName + '.json'), data, (error) => {
			if (error)
				return process.exit(1)
			console.log('done')
			process.exit(0)
		})
	})
// Dependencies
const BlogPosts = require('../models/blogposts.model')
const router = require('express').Router()

// Middleware (example)
router.param('id', (req, res, next, id) => {
	BlogPosts.find({id: id}, (error, obj) => {
		if (error) {
			return res.status(400).json(`Error: No blog post request with id ${id}`);
		}
		req.obj = obj;
	next();
	});
})

/**
 * A get request will currently return all blog post entries that have 
 * been posted to the database.
 */
router.get('/', (req, res) => {
	BlogPosts.find({}, BlogPosts.blogpostObj)
		.then(posts => res.json(posts))
        .catch(err => res.status(400).json('Error: ' + err));
})

// Read single blog post by id
router.get('/:id', (req, res) => {
	blogPosts => res.json(blogPosts);
	res.send(req.obj);
})

// Delete a blog post by id, returns deleted object
router.delete('/:id', (req, res) => {
	req.obj[0].remove((error, results) => {
		if (error)
			return next(error)
		res.send(results)
	});
})

module.exports = router;
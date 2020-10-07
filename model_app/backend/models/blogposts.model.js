const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const blogpostsSchema = new Schema({
  id: {type: Number, required: true},
  title:  {type: String, required: true},
  author: {type: String, required: true},
  body:   {type: String, required: true},
  comments: [{ body: String, author: String, date: Date }],
  date: { type: Date, default: Date.now },
});

// Example object for what to return in a query
// We only select these four fields, plus the ObjectID
const blogpostObj = {
	id: 1,
	title: 'Example Blog Post',
	author: 'The Backend Team',
  body: 'Hello, World! This is the body if the example blog post. Bye.',
};

// Export schema and example object
module.exports = mongoose.model("Blogposts", blogpostsSchema);
module.exports.blogpostObj = blogpostObj;

/*
String category_tag
Date date
String title
String author
String blog_post_text
(link?) comment

*/

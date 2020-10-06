const mongoose = require("mongoose");
const Schema = mongoose.Schema;

  const blogpostsSchema = new Schema({
    id: Number,
    title:  String,
    author: String,
    body:   String,
    comments: [{ body: String, author: String, date: Date }],
    date: { type: Date, default: Date.now },
  });

  const Post = mongoose.model('Post', blogpostsSchema);

/*
String category_tag
Date date
String title
String author
String blog_post_text
(link?) comment

*/

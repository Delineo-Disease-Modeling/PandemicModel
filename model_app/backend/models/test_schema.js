import mongoose from 'mongoose';
  const { Schema } = mongoose;

  const exampleSchema = new Schema({
    title:  String,
    author: String,
    body:   String,
    comments: [{ body: String, author: String, date: Date }],
    date: { type: Date, default: Date.now },
  });

  const Post = mongoose.model('Post', exampleSchema);

/*
String category_tag
Date date
String title
String author
String blog_post_text
(link?) comment

*/

import React from "react";
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import { Link } from 'react-router-dom';
import './BlogPost.css'
 
function BlogPost (props) {
   return (

    <div>
        {/* Hello world */}
       
        
        <title>Built with MongoDB: Interseller | MongoDB Blog</title>
        <meta name="description" content="Interseller is a recruiting tech startup that uses MongoDB to help 4,000 recruiters quickly hire the right candidates. " />
        <meta property="og:site_name" content="MongoDB" />
        <meta property="og:title" content="Built with MongoDB: Interseller | MongoDB Blog" />
        <meta name="og:description" content="Interseller is a recruiting tech startup that uses MongoDB to help 4,000 recruiters quickly hire the right candidates. " />
        <meta property="og:url" content="https://www.mongodb.com/blog/post/built-with-mongodb-interseller" />
        <meta property="og:type" content="article" />
        <meta property="og:image" content="https://webassets.mongodb.com/_com_assets/cms/0 (2)-19amvr4s7p.jpeg" />
        <meta property="og:image:secure_url" content="https://webassets.mongodb.com/_com_assets/cms/0 (2)-19amvr4s7p.jpeg" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:site" content="@mongodb" />
        <meta name="twitter:title" content="Built with MongoDB: Interseller | MongoDB Blog" />
        <meta name="twitter:description" content="Interseller is a recruiting tech startup that uses MongoDB to help 4,000 recruiters quickly hire the right candidates. " />
        <meta name="twitter:image" content="https://webassets.mongodb.com/_com_assets/cms/0 (2)-19amvr4s7p.jpeg" />
        <link rel="alternate" type="application/rss+xml" title="RSS" href="https://www.mongodb.com/blog/rss" />
        <link rel="icon" href="/blog/assets/favicon.ico" type="image/x-icon" />
        <link rel="shortcut icon" href="/blog/assets/favicon.ico" />
        <link rel="stylesheet" type="text/css" href="https://static.mongodb.com/blog/index.7065fd35cc8803bd38d6ae9ddeb9748e.css" />
        <noscript>
          &lt;style&gt;
          .card {'{'}
          opacity: 1 !important;
          transform: none !important
          {'}'}
          &lt;/style&gt;
        </noscript>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.19.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
        <noscript>
          &lt;iframe style="display:none" src="https://www.googletagmanager.com/ns.html?id=GTM-GDFN&amp;nojscript=true"&gt;&lt;/iframe&gt;
        </noscript>
        <div id="mongo-app">
          <main className="app">
            
            <div className="relative w-full overflow-hidden fl fl-center-x fl-wrap">
              <header className="header relative fl fl-center fl-column w-full z-index-10 m-t-70 m-b-10 p-20 h-360">
                <div className="absolute top left w-full h-full" style={{backgroundImage: 'url("https://webassets.mongodb.com/_com_assets/cms/Screen Shot 2020-12-02 at 4.26.35 PM-tfox8tnrhh.png")', backgroundSize: 'cover', backgroundPosition: 'center', backgroundRepeat: 'no-repeat'}} />
                <div className="absolute top left w-full h-full" style={{backgroundColor: 'rgba(0, 0, 0, 0.4)'}} />
                <h1 className="relative white w-max-800 m-h-20 m-t-0 m-b-10 txt-center font-40 font-mobile-25">Blog Title</h1>
                <a href="https://developer.mongodb.com/learn/">
                  <button className="relative btn-green m-5">Link for button!</button>
                </a>
              </header>
              <div className="relative p-h-20 p-v-30 w-full w-max-800">
                <div className="fl fl-wrap fl-center-y m-b-20">
                  <div className="fl fl-wrap p-v-10">
                    <a href="/blog/search/Siya%20Raj%20Purohit">
                      <div className="relative m-r-10 w-50 h-50 b-r-full" style={{backgroundImage: 'url("https://webassets.mongodb.com/_com_assets/cms/Siya-adfnai3e2j.jpg")', backgroundSize: 'cover', backgroundPosition: 'center'}} />
                    </a>
                  </div>
                  <div>
                    <small>
                      <a href="/blog/search/Siya%20Raj%20Purohit">Author Name</a>
                    </small>
                    <br />
                    <small className="post-date">Date of Blog</small>
                    <br />
                    
                  </div>
                </div>
                <div className="cms-content h2-30">
                  <p class="text">
                    We all think our jobs are hard. But if you’re a recruiter, you know just how tough it is to place people into those jobs: the average response rate to recruiters is an abysmal 7%. Enter <a href="https://www.interseller.io/" target="_blank">Interseller</a>
                    , a fast-growing NYC-based SaaS company in the recruiting tech space.
                  </p>
                  <figure>
                    <div className="fl-center">
                      <img src="https://webassets.mongodb.com/_com_assets/cms/Screen Shot 2020-11-30 at 4.03.44 PM-j2fsp8tj33.png" alt=" " title=" " />
                    </div>
                  </figure>
                  <p class="text">
                    For this episode of #BuiltWithMongoDB, we go behind the scenes in recruiting technology with <a href="https://www.linkedin.com/in/stevenlu/" target="_blank">Steven Lu</a>
                    , co-founder and CEO of Interseller.
                  </p>
                  <h4>How did you pick this problem to work on?</h4>
                  <p class="text">While working as an engineer, I helped teach and recruit many other tech professionals. That’s when I realized that good engineers don’t find jobs. They get poached. Sourcing is essential for assembling great teams, but with the low industry response rate, I knew we needed a new solution.</p>
                  <p class="text">I started looking into recruiting technology and was frankly surprised by how outdated the solutions were. We began by addressing three parts of sourcing:</p>
                  <ul>
                    <li>Research</li>
                    <li>Outreach</li>
                    <li>Data Management</li>
                  </ul>
                  <figure>
                    <div className="fl-center">
                      <img src="https://webassets.mongodb.com/_com_assets/cms/Screen Shot 2020-12-02 at 4.06.45 PM-bbv49crcxj.png" alt=" " title=" " />
                    </div>
                  </figure>
                  <p class="text">
                    To help us get started, Interseller went through <a href="https://www.expa.com/" target="_blank">Expa</a>
                    , <a href="https://en.wikipedia.org/wiki/Garrett_Camp" target="_blank">Garrett Camp’s</a>
                    accelerator. We’ve been bootstrapping since then. We’re a team of 13, but we expect to grow to about 25 in another year.
                  </p>
                  <p class="text">We serve about 4,000 recruiters, 75% of whom use us every single day. Some of our customers include Squarespace, Honey, and Compass. Overall, we have had about 2 million candidates respond to us, boosting our average response rate from the industry average of 7% to between 40% and 60%. We attempt to close candidates within 21 days.</p>
                  <h4>How did you decide to have Interseller #BuiltWithMongoDB?</h4>
                  <figure>
                    <div className="fl-center">
                      <img src="https://webassets.mongodb.com/_com_assets/cms/Screen Shot 2020-12-02 at 4.08.21 PM-xy41b57f1w.png" alt=" " title=" " />
                    </div>
                  </figure>
                  <p class="text">Like any engineer, I hate database migrations. I hate having to build around the database rather than the database building around my product. I remember using MongoDB at Compass in 2012—we were a MongoDB shop.</p>
                  <p class="text">After that, I went to another company that was using SQL and a relational database and I felt we were constantly being blocked by database migrations. I had to depend on our CTO to run the database migration before I could merge anything. I have such bad memories from that experience. I would rather have my engineering team push things faster than have to wait on the database side.</p>
                  <p class="text">MongoDB helped solve this. It worked well because it was so adaptable. I don’t know about scaling database solutions since we don’t have millions of users yet, but MongoDB has been a crucial part of getting core functionality, features, and bug fixes out much faster. Outside of MongoDB, we primarily use Node, Javascript, React, and AWS.</p>
                  <p class="text">Our release schedule is really short: as a startup, you have to keep pumping things out, and if half your time is spent on database migration, you won’t be able to serve customers. That’s why MongoDB Atlas is so core to our business. It’s reliable, and I don’t have to deal with database versions.</p>
                  <div className="callout">
                    <p class="text">
                      Building something cool with MongoDB? Check out our <a href="https://developer.mongodb.com/learn/" target="_blank">developer resources</a>
                      , and <a href="https://docs.google.com/forms/d/e/1FAIpQLSeuoc0--D-VbCsR6gBY6FCbwnFMPo0qdP30U8VKc_4or5Jzdg/viewform" target="_blank">let us know</a>
                      if you want your startup to be featured in our #BuiltWithMongoDB series.
                    </p>
                  </div>
                </div>
                <div className="w-full fl fl-center m-v-20">
                  <div className="w-full w-max-300" style={{height: '1px', background: '#D9E0E0'}} />
                  <div className="fl fl-center p-20">
                    <a target="_tab" href="https://www.facebook.com/sharer.php?u=https://www.mongodb.com/blog/post/built-with-mongodb-interseller">
                      <button aria-label="Share on facebook" className="fl fl-center white clickable h-35 w-35 m-h-5 b-r-full reset bg-green hover-fadein-half hover-lift icon-facebook" />
                    </a>
                    <a target="_tab" href="https://www.linkedin.com/shareArticle?mini=true&url=https://www.mongodb.com/blog/post/built-with-mongodb-interseller&title=Built with MongoDB: Interseller&summary=Interseller is a recruiting tech startup that uses MongoDB to help 4,000 recruiters quickly hire the right candidates. &source=MongoDB">
                      <button aria-label="Share on linkedin" className="fl fl-center white clickable h-35 w-35 m-h-5 b-r-full reset bg-green hover-fadein-half hover-lift icon-linkedin" />
                    </a>
                    <a target="_tab" href="https://reddit.com/submit?url=https://www.mongodb.com/blog/post/built-with-mongodb-interseller&title=Built with MongoDB: Interseller">
                      <button aria-label="Share on reddit" className="fl fl-center white clickable h-35 w-35 m-h-5 b-r-full reset bg-green hover-fadein-half hover-lift icon-reddit" />
                    </a>
                    <a target="_tab" href="https://twitter.com/intent/tweet?url=https://www.mongodb.com/blog/post/built-with-mongodb-interseller&text=Built with MongoDB: Interseller">
                      <button aria-label="Share on twitter" className="fl fl-center white clickable h-35 w-35 m-h-5 b-r-full reset bg-green hover-fadein-half hover-lift icon-twitter" />
                    </a>
                  </div>
                  <div className="w-full w-max-300" style={{height: '1px', background: '#D9E0E0'}} />
                </div>
                
                
              </div>
            </div>
           
          </main>
         
        </div>
        <p />
      </div>

       
   );
}

class BackButton {
    handleClick = () => {
        this.props.goBack();
    };

    render() {
        return <Button variant="contained" color="primary" onClick={this.handleClick}>Go Back</Button>;
    }
}

 
export default BlogPost;
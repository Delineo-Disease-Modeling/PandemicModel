import React from 'react';
import './DevelopmentBlog.css'
import { B1Img, B2Img, B3Img } from '../images'

function DevelopmentBlog(props) {
    return(
        <div class='CardBackground'>
            <div class='CardGreenBackground3'>
                <div className="MainHeader">
                    <h2>Development Blog</h2>
                </div>
                
                <div class='row'>
                    <div class='column'>
                         <div class='card1'>
                            <img class='card-img-top' src={B1Img} alt="Blog 1" />
                            <div class="card-body">
                                <h5 className="TitleText">Sample Blog 1</h5>
                                <p class="card-text">Short Discription of blog</p>
                                <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
                            </div>
                        </div>
                     </div>

                    <div class="column">
                        <div class='card1'>
                            <img class='card-img-top' src={B2Img} alt="Blog 2" />
                            <div class="card-body">
                            <h5 className="TitleText">Sample Blog 2</h5>
                            <p class="card-text">Short Discription of blog</p>
                            <p class="card-text"><small class="text-muted">Last updated 1 month ago</small></p>
                            </div>
                        </div>
                    </div>

                    <div class="column">
                        <div class='card1'>
                            <img class='card-img-top' src={B3Img} alt="Blog 3" />
                            <div class="card-body">
                            <h5 className="TitleText">Sample Blog 3</h5>
                            <p class="card-text">Short Discription of blog</p>
                            <p class="card-text"><small class="text-muted">Last updated 2 months ago</small></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}


export default DevelopmentBlog;
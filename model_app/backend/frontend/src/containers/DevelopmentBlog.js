import React from 'react';
import './DevelopmentBlog.css'
import { B1Img, B2Img, B3Img } from '../images'

function DevelopmentBlog(props) {
    return(
        <div className='CardBackground'>
            <div className='CardGreenBackground3'>
                <h2 style={{marginTop: -30+'px'}}>Development Blog</h2>
                
                <div className='row'>
                    <Blog image={B1Img} alt="Blog 1" title="Sample Blog 1" description="Short description of blog" time="3 mins" />

                    <Blog image={B2Img} alt="Blog 2" title="Sample Blog 2" description="Short description of blog" time="1 month" />

                    <Blog image={B3Img} alt="Blog 3" title="Sample Blog 3" description="Short description of blog" time="2 months" />
                </div>
            </div>
        </div>
    );
}

function Blog(props) {
    return <div className="column">
                <div className='card1'>
                    <img className='card-img-top' src={props.image} alt={props.alt} />
                    <div className="card-body">
                    <h5 className="TitleText">{props.title}</h5>
                    <p className="card-text">{props.description}</p>
                    <p className="card-text"><small className="text-muted">Last updated {props.time} ago</small></p>
                    </div>
                </div>
            </div>
}

export default DevelopmentBlog;
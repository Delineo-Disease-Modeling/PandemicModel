import React from 'react';
import {Link} from 'react-router-dom';

function Footer(props) {
    return(
    <div className="footer" style={{backgroundColor:'#68ACE5'}}>
        <div className="container" style={{backgroundColor:'#68ACE5'}}>
            <div className="row justify-content-center">             
                    <div>
                        <h5 style={{color:'white'}}>Our Address</h5>
                        <address>
                        3400 North Charles Street<br />
                        Baltimore, MD 21218<br />
                        The United States<br />
                        </address>
                    </div>

                    <div style={{width:'250px', marginLeft:'20px'}}>
                        <h5 style={{color:'white'}} >Our Contact</h5>
                        <address>
                            <i className="fa fa-phone fa-lg"></i>: 410-516-8775<br />
                        <i className="fa fa-envelope fa-lg"></i>: contactus@cs.jhu.edu<br />
                        <i className="fa fa-globe fa-lg"></i>: <a href="https://engineering.jhu.edu/fields-of-study/computer-science/" style={{ color: '#000' }}>https://engineering.jhu.edu/fields-of-study/computer-science/</a>
                        </address>
                    </div>
                <div className="col-12 col-sm-4 align-self-center" style={{marginLeft:'-40px'}}>
                    <div className="text-center">
                        <a className="btn btn-social-icon btn-google" href="http://google.com/+"><i className="fa fa-google-plus"></i></a>
                        <a className="btn btn-social-icon btn-facebook" href="http://www.facebook.com/profile.php?id="><i className="fa fa-facebook"></i></a>
                        <a className="btn btn-social-icon btn-linkedin" href="http://www.linkedin.com/in/"><i className="fa fa-linkedin"></i></a>
                        <a className="btn btn-social-icon btn-twitter" href="http://twitter.com/"><i className="fa fa-twitter"></i></a>
                        <a className="btn btn-social-icon btn-google" href="http://youtube.com/"><i className="fa fa-youtube"></i></a>
                    </div>
                </div>
            </div>
            <div className="row justify-content-center">             
                <div className="col-auto" style={{marginTop:'10px'}}>
                    <p>© Copyright</p>
                </div>
            </div>
        </div>
    </div>
    )
}

export default Footer;
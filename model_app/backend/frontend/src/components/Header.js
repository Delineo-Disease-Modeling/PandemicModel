import React from 'react';
import dotImage from '../images/dots.jpg'

function Header(props) {
    return <div>
        <h3 style={{marginTop:'1%'}}>{props.text}</h3>
        <img src={dotImage} alt="dots"></img>
    </div>;
}

export default Header;
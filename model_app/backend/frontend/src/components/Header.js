import React from 'react';


function Header(props) {
    return <div>
        <h3 style={{marginTop:'1%'}}>{props.text}</h3>
    </div>;
}

export default Header;
import React from 'react';
import { County, Timeseries, GoogleMap } from '../components';

function Simulator(props) {
    return(
        <div className="container">
            <County/>
            <GoogleMap/>
            <Timeseries/>
        </div>
    );
}

export default Simulator;
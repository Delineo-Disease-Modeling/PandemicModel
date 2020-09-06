import React from 'react';
import SimpleLineChart from './LineChart.js';

const formatString = (str) => {
    return str.substring(1, str.length-1).replace(/ /g, '').split(',').map(Number);
}

function SimulationTimeseries(props) {
    //convert into array 
    const infected = formatString(props.infected);
    const deaths = formatString(props.deaths);

    const data = infected.map((d,i) => {
        return { name: i, infected: d, deaths: deaths[i] }
    });

    return <SimpleLineChart data = {data} width = {800} height = {500}/>;
}

export default SimulationTimeseries;

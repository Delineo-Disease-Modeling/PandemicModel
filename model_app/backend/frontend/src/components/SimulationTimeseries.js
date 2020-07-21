import React from 'react';
import { Container } from 'reactstrap';
import LineChart from './LineChart.js';

function SimulationTimeseries(props) {
    return (
            <Container>
                <div style={{marginBottom:'40px'}}>
                    <h5 style={{color:'#66FCF1'}}>Expected Infection Rate</h5>
                    <LineChart data = {props.infected} width = {800} height = {500}/>
                </div>
                
                <div style={{margin:'20px'}}>
                    <h5 style={{color:'#66FCF1'}}>Expected Death Rate</h5>
                    <LineChart data = {props.deaths} width = {800} height = {500}/>
                </div>
                
            </Container>
        );
}

export default SimulationTimeseries;

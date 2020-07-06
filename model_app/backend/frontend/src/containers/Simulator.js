import React from 'react';
import { County, Timeseries, GoogleMap } from '../components';
import './Simulator.css'


function Paramaeters(){
    return(

    <div>

        <div class='row'>
            <div class='col'>
                <table>
                    <tbody>

                        <tr>
                            <td>
                                <label class='label'>Simulation duration (days):</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='20'></input>
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label class='label'>Other Parameters:</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='20'></input>
                            </td>
                        </tr>

                    </tbody>
                </table>
                
            </div>

            <div class='col'> 

                <table>
                    <tbody>

                        <tr>
                            <td>
                                <label class='label'>Infection duration (days):</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='20'></input>
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label class='label'>Other Parameters:</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='20'></input>
                            </td>
                        </tr>

                    </tbody>
                </table>

            </div>
        </div>

    </div> 
    );
}

function Simulator(props) {
    return(
        <div class='CardBackground'>

            <div class='GreenBackground'>
                <h3>Map</h3>
                <County/>
                <GoogleMap/> 
            </div>

            <div class='GreenBackground'>
                <h3>Configurations</h3>
                <p style={{textAlign:'left', fontSize:'20px', color:'#66FCF1'}}>Model Parameters</p>
                <Paramaeters/>
                <p style={{textAlign:'left', fontSize:'20px', color:'#66FCF1', marginTop:'20px'}}>Intervention Policy</p>
            </div>
            
            <div class='GreenBackground'>
                <h3>Analysis</h3>
                <Timeseries/>
            </div>



            
        </div>
    );
}

export default Simulator;
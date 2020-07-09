import React, {Component} from 'react';
import '../containers/Simulator.css'

function Parameters(){
    return(

    <div>

        <div className='row'>
            <div className='col'>
                <table>
                    <tbody>

                        <tr>
                            <td>
                                <label className='label'>Simulation duration (days):</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='15'></input>
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label className='label'>Other Parameters:</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='15'></input>
                            </td>
                        </tr>

                    </tbody>
                </table>
                
            </div>

            <div className='col'> 

                <table>
                    <tbody>

                        <tr>
                            <td>
                                <label className='label'>Infection duration (days):</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='15'></input>
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label className='label'>Other Parameters:</label>
                            </td>
                            <td>
                                <input required minLength='6' type='text' size='15'></input>
                            </td>
                        </tr>

                    </tbody>
                </table>

            </div>
        </div>

    </div> 
    );
}

export default Parameters;
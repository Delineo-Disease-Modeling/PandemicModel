import React from 'react';
import '../containers/Simulator.css'
import Slider from '@material-ui/core/Slider'
import {withStyles, makeStyles} from '@material-ui/core/styles';

import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
//import {MuiPickersUtilsProvider, KeyboardDatePicker} from '@material-ui/core/pickers';



//used to change various styles of the slider
const DaySlider = withStyles({
    root: {
        color: '#ffbb00',


    },
})(Slider);




//just a place holder for now for returning the values
const getValue = (e,val) => {
    console.warn(val)
}

function Parameters(){
    const [value, setValue] = React.useState('female');

    const handleChange = (event) => {
      setValue(event.target.value);
    };

    return(

    <div>

        <div className='row'>
            <div className='col'>

                <table>
                    <tbody>

                        <tr>
                            <td>
                                <label className='label' >Simulation duration (days):</label>
                            </td>
                            <td>
                                <Slider
                                    min = {1}
                                    max = {12}
                                    valueLabelDisplay ="auto"
                                    onChangeCommitted = {getValue}
                                > </Slider>
                            </td>
                        </tr>

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
                                <label className='label'>Social Distancing Scale:</label>
                            </td>
                            <td>
                                <Slider
                                    min = {1}
                                    max = {5}
                                    valueLabelDisplay ="auto"
                                    //onChangeCommitted = insert function here to pass data
                                  />
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label className='label'>Population Size:</label>
                            </td>
                            <td>
                                <Slider
                                    min = {1}
                                    max = {5}
                                    valueLabelDisplay ="auto"
                                    //onChangeCommitted = insert function here to pass data
                                  />
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label className='label'>Capacity:</label>
                            </td>
                            <td>
                                <Slider
                                    min = {1}
                                    max = {5}
                                    valueLabelDisplay ="auto"
                                    //onChangeCommitted = insert function here to pass data
                                  />
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label className='label'>Density:</label>
                            </td>
                            <td>
                                <Slider
                                    min = {1}
                                    max = {5}
                                    valueLabelDisplay ="auto"
                                    //onChangeCommitted = insert function here to pass data
                                  />
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label className='label'>Mobility:</label>
                            </td>
                            <td>
                                <FormControl component="fieldset">

                                  <RadioGroup aria-label="mobility" name="mobility1" value={value} onChange={handleChange} row = {true}>
                                    <FormControlLabel className ='label' value="1" control={<Radio />} label="1" />
                                    <FormControlLabel className ='label' value="2" control={<Radio />} label="2" />
                                    <FormControlLabel className ='label' value="3" control={<Radio />} label="3" />
                                    <FormControlLabel className ='label' value="4" control={<Radio />} label="4" />
                                  </RadioGroup>
                                </FormControl>
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <label className='label'>Mask Wearing (%):</label>
                            </td>
                            <td>
                                <Slider
                                    min = {0}
                                    max = {100}
                                    valueLabelDisplay ="auto"
                                    //onChangeCommitted = insert function here to pass data
                                  />
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

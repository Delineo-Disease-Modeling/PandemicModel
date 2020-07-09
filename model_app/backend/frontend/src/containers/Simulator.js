import React, {Component} from 'react';
import { County, Timeseries, GoogleMap} from '../components';
import './Simulator.css'
import axios from 'axios';
import Parameters from '../components/ConfigurationParameters.js'
import OptionMenu from '../components/OptionMenu.js'


class Simulator extends Component{

    constructor(){
        super();
        this.state={
            hidden:false,
            policy:'',
            loading: false,
            data: '',
            jobId: null
        }
    }

    handleOnClick = () => {
        // if user had an existing job request, delete that 
        if (this.state.jobId) {
            axios.delete(`./simulations/${this.state.jobId}`)
                .catch(err => console.log(err) );
        }

        // configure post body with specific model params
        let body = {};

        // send post request
        axios.post('./simulations', body)
            .then(res => {
                // only upon successful post request, update state with in progress state and 
                if (res.status === 200) {
                    this.setState({jobId: `${res.data}`, loading: true});
                    console.log('post sent with job id ' + res.data);

                    axios.get(`./simulations/${res.data}`)
                        .then(result => {
                            this.setState({
                                loading: false,
                                data: [...result.data],
                            });

                            console.log('simulation finished running');
                        })
                        .catch(err => {
                            console.log(err);
                        });

                    // should probably save data to redux store
                    // maybe also save jobId? idk yet
                }
            })
            .catch(err => {
                console.log(err);
                throw err;
            });
    }


    render(){
        const {data, loading} = this.state;

        return(
            <div className='CardBackground'>

                <div className='GreenBackground'>
                    <h3>Map</h3>
                    <County/>
                    <GoogleMap/> 
                </div>

                <div className='GreenBackground'>
                    <h3>Configurations</h3>
                    <p style={{textAlign:'left', fontSize:'20px', color:'#66FCF1'}}>Model Parameters</p>
                    <Parameters/>
                    <p style={{textAlign:'left', fontSize:'20px', color:'#66FCF1', marginTop:'20px'}}>Intervention Policy</p>

                    <OptionMenu/>

                    
                    <br></br>
                    <button className='button' onClick={this.handleOnClick}>Run Simulation</button>

                </div>
                
                {loading ? <p>loading...</p> :
                <div className='GreenBackground'>
                    <h3>Analysis</h3>
                    <p>{data}</p>
                    <Timeseries/>
                </div>
                }
                
            </div>
        );

    }

}

export default Simulator;
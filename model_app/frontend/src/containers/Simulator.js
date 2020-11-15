import React, { Component } from 'react';
import { Place, GoogleMap, Parameters, OptionMenu, SimulationTimeseries, PersistentDrawerLeft } from '../components';
import './Simulator.css'
import axios from 'axios';
import Button from '@material-ui/core/Button';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import {withStyles} from '@material-ui/core/styles';

const ColoredAccordion = withStyles({
    root: {
        backgroundColor: '#1b4441c2',
        fontSize: '20px',
        color: '#66FCF1'



    },
})(Accordion);

class Simulator extends Component {

    constructor() {
        super();
        this.state = {
            hidden: false,
            policy: '',
            data: [],
            loading: false,
            jobId: null,
        };
        this._isMounted = false;
    }

    componentDidMount() {
        this._isMounted = true;
        this.source = axios.CancelToken.source();
    }

    handleOnClick = () => {
        // if user had an existing job request, delete that
        if (this.state.jobId) {
            axios.delete(`./simulations/${this.state.jobId}`, { cancelToken: this.source.token })
                .catch(err => {
                    if (axios.isCancel(err)) {
                        console.log('Request canceled:', err.message);
                    } else { console.log(err) }
                });
        }

        // configure post body with specific model params
        let body = {};

        // send post request
        axios.post('./simulations', body, { cancelToken: this.source.token })
            .then(res => {
                // only upon successful post request, update state with in progress state and
                if (res.status === 200) {
                    this._isMounted && this.setState({ jobId: `${res.data}`, loading: true });
                    console.log('post sent with job id ' + res.data);

                    axios.get(`./simulations/${res.data}`, { cancelToken: this.source.token })
                        .then(result => {
                            this._isMounted && this.setState({ loading: false, data: [...result.data] });
                            console.log('simulation finished running');
                        })
                        .catch(err => {
                            if (axios.isCancel(err)) {
                                console.log('Request canceled:', err.message);
                            } else { console.log(err) }
                        });

                    // should probably save data to redux store
                    // maybe also save jobId? idk yet
                }
            })
            .catch(err => {
                if (axios.isCancel(err)) {
                    console.log('Request canceled:', err.message);
                } else { console.log(err) }
            });
    }

    componentWillUnmount() {
        this._isMounted = false;
        this.source.cancel('Operation canceled by the user.');

        // remove existing job request, if it existed
        if (this.state.jobId) {
            axios.delete(`./simulations/${this.state.jobId}`)
                .catch(err => console.log(err));
        }
    }
    //<p style={{ textAlign: 'left', fontSize: '20px', color: '#66FCF1' }}>Model Parameters</p>

    render() {
        const { data, jobId, loading } = this.state;

        // no timeseries: replace with simulation timeseries
        return (
            <div className='GreenBackground'>
                <PersistentDrawerLeft runOnClick={this.handleOnClick}>
                    <div className='GreenBackground'>
                        <h3>Map</h3>
                        <Place />
                        <GoogleMap />
                    </div>

                    <div>
                        <div className='GreenBackground'>
                            <h3>Configurations</h3>


                            <ColoredAccordion>
                              <AccordionSummary
                                  expandIcon={<ExpandMoreIcon />}
                                  aria-controls="Model Param-content"
                                  id="Model Param-header"
                              >
                                Model Parameters
                              </AccordionSummary>
                                <Parameters />
                            </ColoredAccordion>
                            <br></br>
                            <ColoredAccordion>
                              <AccordionSummary
                                  expandIcon={<ExpandMoreIcon />}
                                  aria-controls="Intervention Policy-content"
                                  id="Intervention Policy-header"
                              >
                                Intervention Policy
                              </AccordionSummary>
                                <OptionMenu />
                            </ColoredAccordion>

                            <br></br>

                            <Button variant="contained" color="primary" className='button' onClick={this.handleOnClick}>
                                Run Simulation                            
                            </Button>
                        </div>
                    </div>

                    <div>
                        {jobId ? (loading ? <p>loading...</p> :
                            <div className='GreenBackground'>
                                <h3>Analysis</h3>
                                <SimulationTimeseries infected={data[1]} deaths={data[2]} />
                            </div>)
                            : null}
                    </div>
                </PersistentDrawerLeft>
            </div>
        );
    }

}

export default Simulator;

import React, { Component } from 'react';
import {Container } from 'reactstrap';
import { connect } from 'react-redux';
import { getTimeseries } from '../actions/timeseriesActions.js';
import PropTypes from 'prop-types';
import LineChart from './LineChart.js';

class Timeseries extends Component {
    constructor(props) {
        super(props);
        this.state = {start: "02-25-20", end: "05-03-20"}
        this.fips = 1001;
    }

    componentDidMount() {
        this.props.getTimeseries(this.fips, this.state.start, this.state.end);
    }

    componentDidUpdate(prevProps) {
        if (this.props.demographics !== prevProps.demographics) {
            const {FIPS} = this.props.demographics;
            this.props.getTimeseries(FIPS, this.state.start, this.state.end);
            this.fips = FIPS;
        }
    }

    render() {
        const timeseries = this.props.timeseries;

        const infected = timeseries.map((item) => {
            return { date: new Date(`${item.date}`), value: Number(`${item[this.fips].infected}`) };
        })
        const death = timeseries.map((item) => {
            return { date: new Date(`${item.date}`), value: Number(`${item[this.fips].death}`) };
        })

        return (
            <Container>
                <div style={{marginBottom:'40px'}}>
                    <h5 style={{color:'#66FCF1'}}>Infection Rate</h5>
                    <LineChart data = {infected} width = {800} height = {500}/>
                </div>
                
                <div style={{margin:'20px'}}>
                    <h5 style={{color:'#66FCF1'}}>Death Rate</h5>
                    <LineChart data = {death} width = {800} height = {500}/>
                </div>
                
            </Container>
        );
    }
}

Timeseries.propTypes = {
    getTimeseries: PropTypes.func.isRequired,
    timeseries : PropTypes.array.isRequired,
}

const mapStateToProps = (state) => ({
    timeseries: state.timeseries,
    demographics: state.demographics
});

// first param of connect: mapStateToProp since state is immutable in Redux Architecture
// Second param of connect is actions necessary for the component
export default connect(mapStateToProps, { getTimeseries })(Timeseries);

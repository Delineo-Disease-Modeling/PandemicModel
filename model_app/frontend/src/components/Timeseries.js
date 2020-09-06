import React, { Component } from 'react';
import { connect } from 'react-redux';
import { getTimeseries } from '../actions/timeseriesActions.js';
import PropTypes from 'prop-types';
import SimpleLineChart from './LineChart.js';

class Timeseries extends Component {
    constructor(props) {
        super(props);
        this.state = {start: "02-25-20", end: "05-03-20"}
        this.fips = this.props.demographics ? this.props.demographics.FIPS : 1001;
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

        const data = timeseries.map((item) => {
            return { name: `${item.date}`.substring(5,10), infected: Number(`${item[this.fips].infected}`),
                deaths: Number(`${item[this.fips].death}`) };
        });

        return (
            <SimpleLineChart data = {data} width = {800} height = {500}/>
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

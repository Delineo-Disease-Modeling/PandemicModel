import React, { Component } from 'react';
import {Container, ListGroup, ListGroupItem } from 'reactstrap';
import {CSSTransition, TransitionGroup } from "react-transition-group";
import { connect } from 'react-redux';
import { getTimeseries } from '../actions/timeseriesActions.js';
import PropTypes from 'prop-types';
import LineChart from './LineChart.js'

class Timeseries extends Component {
    constructor(props) {
        super(props);
        this.state = {fips: 1001, start: "02-25-20", end: "05-03-20"}
    }
    componentDidMount() {
        this.props.getTimeseries(this.state.fips, this.state.start, this.state.end);
    }

    render() {
        const {timeseries} = this.props.timeseries;
        const infected = timeseries.map((item) => {
            return { date: new Date(`${item.date}`), value: Number(`${item[this.state.fips].infected}`) };
        })
        const death = timeseries.map((item) => {
            return { date: new Date(`${item.date}`), value: Number(`${item[this.state.fips].death}`) };
        })

        return (
            <Container>
                <LineChart data = {infected} width = {800} height = {500}/>
                <LineChart data = {death} width = {800} height = {500}/>
                <ListGroup>
                {timeseries.map((item) => (
                        <ListGroupItem key={item._id}>
                            The date is: {item.date}, number infected is: {item[this.state.fips].infected},
                            and number deaths is: {item[this.state.fips].death}
                        </ListGroupItem>
                        ))}
                </ListGroup>
            </Container>
        );
    }
}

Timeseries.propTypes = {
    getTimeseries: PropTypes.func.isRequired,
    timeseries : PropTypes.object.isRequired,
}

const mapStateToProps = (state) => ({
    timeseries: state.timeseries
});

// first param of connect: mapStateToProp since state is immutable in Redux Architecture
// Second param of connect is actions necessary for the component
export default connect(mapStateToProps, { getTimeseries })(Timeseries);

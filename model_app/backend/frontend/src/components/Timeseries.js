import React, { Component } from 'react';
import {Container, ListGroup, ListGroupItem } from 'reactstrap';
import {CSSTransition, TransitionGroup } from "react-transition-group";
import { connect } from 'react-redux';
import { getTimeseries } from '../actions/timeseriesActions.js';
import PropTypes from 'prop-types';

class Timeseries extends Component {
    constructor(props) {
        super(props);
        this.state = {fips: 1001, start: "4-27-20", end: "05-03-20"}
    }
    componentDidMount() {
        this.props.getTimeseries(this.state.fips, this.state.start, this.state.end);
    }

    render() {
        const {timeseries} = this.props.timeseries;

        return (
            <Container>
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

// <TransitionGroup className={"timeseries"}>
//                         {timeseries.map((item) => (
//                             //<CSSTransition key={_id} timeout={500} classNames={'fade'}>
//                                 <ListGroupItem>
//                                     The date is: {item.date}
//                                 </ListGroupItem>
//                             </CSSTransition>
//                         ))}
//                     </TransitionGroup>

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

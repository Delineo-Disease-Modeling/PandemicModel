import React, { Component } from 'react';
import {Container, ListGroup, ListGroupItem, Button } from 'reactstrap';
import {CSSTransition, TransitionGroup } from "react-transition-group";
import { connect } from 'react-redux';
import { getCounties } from '../actions/countyActions';
import PropTypes from 'prop-types';

class County extends Component {

    componentDidMount() {
        this.props.getCounties();
    }

    render() {
        const { counties } = this.props.county;

        return (
            <Container>
                <ListGroup>
                    <TransitionGroup className={"county"}>
                        {counties.map(({_id, FIPS, Area_Name}) => (
                            <CSSTransition key={_id} timeout={500} classNames={'fade'}>
                                <ListGroupItem>
                                    The county with FIPS: {FIPS} is in {Area_Name}
                                </ListGroupItem>
                            </CSSTransition>
                        ))}
                    </TransitionGroup>
                </ListGroup>
            </Container>
        );
    }
}

County.propTypes = {
    getCounties: PropTypes.func.isRequired,
    county : PropTypes.object.isRequired
}

const mapStateToProps = (state) => ({
    county: state.county
});

// first param of connect: mapStateToProp since state is immutable in Redux Architecture
// Second param of connect is actions necessary for the component
export default connect(mapStateToProps, { getCounties })(County);

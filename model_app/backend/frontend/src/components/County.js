import React, { Component } from 'react';
import {Container, ListGroup, ListGroupItem } from 'reactstrap';
import { connect } from 'react-redux';
import { getDemographics } from '../actions/demographicsActions';
import PropTypes from 'prop-types';
import GoogleMap from './GoogleMap.js';

class County extends Component {
    constructor(props) {
        super(props);
        this.state = {fips: 1001};
    }

    componentDidMount() {
        this.props.getDemographics(this.state.fips);
    }

    render() {
        const { demographics } = this.props.demographics;
        return (
            <Container>
                <ListGroup>
                    <ListGroupItem>
                        The county with FIPS: {demographics.FIPS} is in {demographics.Area_Name} and 
                        has population {demographics.POP_ESTIMATE_2018}
                    </ListGroupItem>
                </ListGroup>
                <GoogleMap/>
            </Container>
        );
    }
}


County.propTypes = {
    getDemographics: PropTypes.func.isRequired,
    demographics : PropTypes.object.isRequired,
}

const mapStateToProps = (state) => ({
    demographics: state.demographics,
    county: state.county
});

// first param of connect: mapStateToProp since state is immutable in Redux Architecture
// Second param of connect is actions necessary for the component
export default connect(mapStateToProps, { getDemographics })(County);

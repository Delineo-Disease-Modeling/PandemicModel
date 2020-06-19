import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
import * as d3 from 'd3';

class Axis extends Component {
    componentDidMount() {
        this.renderAxis();
    }

    componentDidUpdate() {
        this.renderAxis();
    }

    renderAxis() {
        const node = ReactDOM.findDOMNode(this);
        d3.select(node).call(this.props.axis)
        .attr("transform", (this.props.axisType=='x') ?
            `translate(0, ${this.props.height})` :
            `translate(${this.props.width}, 0)` );
    }

    render() {
        return <g className="axis"></g>;
    }
}

Axis.propTypes = {
    height: PropTypes.number.isRequired,
    width: PropTypes.number.isRequired,
    axis: PropTypes.func.isRequired,
    axisType : PropTypes.oneOf(['x','y']).isRequired
}

export default Axis;
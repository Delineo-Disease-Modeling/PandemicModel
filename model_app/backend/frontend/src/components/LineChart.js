import React, { Component } from 'react';
import * as d3 from 'd3';

class LineChart extends Component {
    constructor(props) {
        super(props);
        this.createLineChart = this.createLineChart.bind(this);
    }

    componentDidMount() {
        this.createLineChart();
    }

    componentDidUpdate() {
        this.createLineChart();
    }

    createLineChart() {
        const node = this.node;
        const data = this.props.data;
        const width = this.props.width;
        const height = this.props.height;
        const margin = ({top: 20, right: 30, bottom: 30, left: 40});

        console.log(data)
        const x = d3.scaleUtc()
            .domain(d3.extent(data, d => d.date))
            .range([margin.left, width - margin.right]);
        const y = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)]).nice()
            .range([height - margin.bottom, margin.top]);
        let line = d3.line()
            .x(d => x(d.date))
            .y(d => y(d.value));

        d3.select(node)
            .append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("d", line);
    }

    render() {
        return <svg ref={node => this.node = node} width={500} height={500}></svg>;
    }
}

export default LineChart;
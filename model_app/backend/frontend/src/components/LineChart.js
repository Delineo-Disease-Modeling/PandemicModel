import React, { Component } from 'react';
import * as d3 from 'd3';
import './LineChart.css'

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
        let data = this.props.data;
        const width = this.props.width;
        const height = this.props.height;
        const margin = ({top: 20, right: 20, bottom: 30, left: 30});

        let x = () => {};
        let y = () => {};
        let line = () => {};

        // this is for timeseries
        if (data instanceof Object) {
            x = d3.scaleUtc()
                .domain(d3.extent(data, d => d.date))
                .range([margin.left, width - margin.right]);
            y = d3.scaleLinear()
                .domain([0, d3.max(data, d => d.value)]).nice()
                .range([height - margin.bottom, margin.top]);
            line = d3.line()
                .x(d => x(d.date))
                .y(d => y(d.value));

        }
        else { // this is for simulationTimeseries
            // convert data from string to array
            data = data.substring(1, data.length-1).replace(/ /g, '').split(',').map(Number);
            x = d3.scaleLinear()
                .domain([0, data.length])
                .range([margin.left, width - margin.right]);
            y = d3.scaleLinear()
                .domain(d3.extent(data)).nice()
                .range([height - margin.bottom, margin.top]);
            line = d3.line()
                .x((d,i) => x(i))
                .y(d => y(d));
        };

        const xAxis = g => 
            g.attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0));

        const yAxis = g => 
            g.attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y).ticks(null, "s"))
            .call(g => g.select(".domain").remove())
            .call(g => g.select(".tick:last-of-type text").clone()
                .attr("x", 3)
                .attr("text-anchor", "start")
                .attr("font-weight", "bold")
                .text(data.y));

        //clear old chart
        d3.select(node).selectAll("*").remove()

        // add line
        d3.select(node)
            .append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "#66FCF1")
            .attr("stroke-width", 2)
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("d", line);

        // add x axis
        d3.select(node)
            .append("g")
            .call(xAxis)
            .attr("class", "axis")
            .selectAll("text")
            .style("fill", "#ffffff");

        // add y axis
        d3.select(node)
            .append("g")
            .call(yAxis)
            .attr("class", "axis")
            .selectAll("text")
            .style("fill", "#ffffff");
    }

    render() {
        const height = this.props.height;
        const width = this.props.width;
        return <svg ref={node => this.node = node} width={width} height={height}></svg>;
    }
}

export default LineChart;
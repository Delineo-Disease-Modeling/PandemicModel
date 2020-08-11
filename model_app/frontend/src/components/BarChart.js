import React, { Component } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';

class SimpleBarChart extends Component {
    renderColorfulLegendText(value, entry) {
        const { color } = entry;
        return <span style={{ color }}>{value}</span>;
    }

    render() {
        const {width, height, data} = this.props;
        return (
            <BarChart width={width} height={height} data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5, }}>
    <XAxis dataKey="name" interval="preserveStartEnd"/>
            <YAxis interval="preserveStartEnd"/>
            <Tooltip />
            <Legend formatter={this.renderColorfulLegendText}/>
        <Bar layout="horizontal" dataKey="infected" fill="#8884d8"/>
            <Bar layout="horizontal" dataKey="deaths" fill="#82ca9d" />
            </LineChart>
    );
    }
}

export default SimpleBarChart;
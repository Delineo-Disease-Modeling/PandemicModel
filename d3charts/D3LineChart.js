// D3 source code for line chart that can pan and zoom
// Run in Observable
// Adapted from https://observablehq.com/@d3/zoomable-area-chart?collection=@d3/d3-zoom

/*
Chart components using d3 math:
- <g> xAxis
- <g> yAxis
- <path> line

React stuff
- clipPath -> update xAxis, line
- rescale -> update xAxis
*/

chart = {
  const zoom = d3.zoom()
      .scaleExtent([1, 32])
      .extent([[margin.left, 0], [width - margin.right, height]])
      .translateExtent([[margin.left, -Infinity], [width - margin.right, Infinity]])
      .on("zoom", zoomed);

  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height]);

  const clip = DOM.uid("clip");

  svg.append("clipPath")
      .attr("id", clip.id)
    .append("rect")
      .attr("x", margin.left)
      .attr("y", margin.top)
      .attr("width", width - margin.left - margin.right)
      .attr("height", height - margin.top - margin.bottom);

  const path = svg.append("path")
      .datum(data)
      .attr("clip-path", clip)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("d", line(data, x));

  const gx = svg.append("g")
      .call(xAxis, x);

  svg.append("g")
      .call(yAxis, y);

  svg.call(zoom)
    .transition()
      .duration(750)
      .call(zoom.scaleTo, 4, [x(Date.UTC(2001, 8, 1)), 0]);

  function zoomed() {
    const xz = d3.event.transform.rescaleX(x);
    path.attr("d", line(data, xz));
    gx.call(xAxis, xz);
  }

  return svg.node();
}


height = 500

margin = ({top: 20, right: 20, bottom: 30, left: 30})

x = d3.scaleUtc()
    .domain(d3.extent(data, d => d.date))
    .range([margin.left, width - margin.right])

y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)]).nice()
    .range([height - margin.bottom, margin.top])

xAxis = (g, x) => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))

yAxis = (g, y) => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(null, "s"))
    .call(g => g.select(".domain").remove())
    .call(g => g.select(".tick:last-of-type text").clone()
        .attr("x", 3)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text(data.y))

line = (data, x) => d3.line()
    .curve(d3.curveStepAfter)
    .x(d => x(d.date))
    .y(d => y(d.value))

//data and d3 required
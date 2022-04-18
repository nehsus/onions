import { useD3 } from './useD3';
import React from 'react';
import * as d3 from 'd3';

/**
 * Charted from:
 * https://www.pluralsight.com/guides/using-d3.js-inside-a-react-app
 * @param {*} { data }
 * @returns .svg
 */
function Chart({ data }) {
  const ref = useD3(
    (svg) => {
      const height = 500;
      const width = 500;
      const margin = { top: 40, right: 30, bottom: 30, left: 40 };
      
      var xdata = ["","", "Opinion", "distilBERT", "RMP"];

      const x = d3
        .scaleBand()
        .domain(data.map((d) => d.year))
        .rangeRound([50, 200])
        .padding(0.1);

      const y1 = d3
        .scaleLinear()
        .domain([0, 5])
        .rangeRound([height - margin.bottom, margin.top]);

      const xAxis = (g) =>
        g.attr("transform", `translate(0,${height - margin.bottom})`).call(
          d3
            .axisBottom(x)
            .tickSize(15)
            .tickValues(
              d3
                .ticks(...d3.extent(x.domain()), width / margin.left)
                .filter((v) => x(v) !== undefined)
            )
            .tickSizeOuter(0)
            .tickFormat(function (d) {
                return xdata[d];
            })
        );

      const y1Axis = (g) =>
        g
          .attr("transform", `translate(${margin.left},0)`)
          .style("color", "steelblue")
          .call(d3.axisLeft(y1).ticks(null, "s"))
          

      svg.select(".x-axis").call(xAxis);
      svg.select(".y-axis").call(y1Axis);

      svg
        .select(".plot-area")
        .attr("fill", "steelblue")
        .selectAll(".bar")
        .attr("class", "chart")
      .classed("svg-content-responsive", true)
        .data(data)
        .join("rect")
        .attr("class", "bar")
        .attr("x", (d) => x(d.year))
        .attr("width", x.bandwidth())
        .attr("y", (d) => y1(d.sales))
        .attr("height", (d) => y1(0) - y1(d.sales));
    },
    [data.length]
  );

  return (
    <svg
      ref={ref}
      style={{
        height: 500,
        width: '100%',
        marginRight: "0px",
        marginLeft: "20px",
        paddingTop: "40px"
      }}
    >
      <g className="plot-area" />
      <g className="x-axis" />
      <g className="y-axis" />
    </svg>
    
  );
}

export default Chart;
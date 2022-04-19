import { useD3 } from './useD3';
import React from 'react';
import * as d3 from 'd3';

/**
 * Charted from:
 * https://www.pluralsight.com/guides/using-d3.js-inside-a-react-app
 * @param {*} { data }
 * @returns .svg
 */
function ChartUniversity(data) {
    // useEffect(() => {
    //     drawChart(svg);
    //   }, [data]);
  const ref = useD3(
    (svg) => {
        const margin = {
            top: 50, right: 50, bottom: 50, left: 50,
          };
        
          const width = 2 * 100 + margin.left + margin.right;
          const height = 2 * 200 + margin.top + margin.bottom;
        
          const colorScale = d3     
            .scaleSequential()      
            .interpolator(d3.interpolateCool)      
            .domain([0, data.length]);
        
          
        
          function drawChart(svgs) {
            // Remove the old svg
            d3.select('#pie-container')
              .select('svg')
              .remove();
        
            // Create new svg
            const svg = d3
              .select('#pie-container')
              .append('svg')
              .attr('width', width)
              .attr('height', height)
              .append('g')
              .attr('transform', `translate(${width / 2}, ${height / 2})`);
        
            const arcGenerator = d3
              .arc()
              .innerRadius(100)
              .outerRadius(200);
        
            const pieGenerator = d3
              .pie()
              .padAngle(0)
              .value((d) => d.value);
        
            const arc = svgs
              .selectAll()
              .data(pieGenerator(data))
              .enter();
        
            // Append arcs
            arc
              .append('path')
              .attr('d', arcGenerator)
              .style('fill', (_, i) => colorScale(i))
              .style('stroke', '#ffffff')
              .style('stroke-width', 0);
        
            // Append text labels
            arc
              .append('text')
              .attr('text-anchor', 'middle')
              .attr('alignment-baseline', 'middle')
              .text((d) => d.data.label)
              .style('fill', (_, i) => colorScale(data.length - i))
              .attr('transform', (d) => {
                const [x, y] = arcGenerator.centroid(d);
                return `translate(${x}, ${y})`;
              });
          }    

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
      <g className="pie-container" />
    </svg>
    
    );
  },[data.length]
  );
}

export default ChartUniversity;

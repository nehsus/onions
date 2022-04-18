import React from 'react';
import * as d3 from 'd3';

/**
 * React hook for chart:
 * https://www.pluralsight.com/guides/using-d3.js-inside-a-react-app
 * @param {*} renderChartFn 
 * @param {*} dependencies 
 * @returns ref
 */
export const useD3 = (renderChartFn, dependencies) => {
    const ref = React.useRef();

    React.useEffect(() => {
        renderChartFn(d3.select(ref.current));
        return () => {};
      }, dependencies);
    return ref;
}
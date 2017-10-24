function drawGraph(graph, config) {
    var rowIndex = Math.floor(config.index / config.cntPerRow);
    var columnIndex = config.index % config.cntPerRow;
    var y0 = rowIndex * config.cellWidth;
    var x0 = columnIndex * config.cellWidth;
    var svg = d3.select('#canvas');

    svg.append('rect')
        .attr('x', x0)
        .attr('y', y0)
        .attr('width', config.cellWidth)
        .attr('height', config.cellWidth)
        .attr('fill', 'none')
        .attr('stroke', '#cccccc')
        .attr('stroke-width', '1px');

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var simulation = d3.forceSimulation()
        .force('link', d3.forceLink().id(function(d) { return d.id; }))
        .force('charge', d3.forceManyBody().strength(-3000))
        .force('center', d3.forceCenter(x0 + config.cellWidth / 2, y0 + config.cellWidth / 2));

    var link = svg.append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(graph.links)
        .enter().append('line')
        .attr('stroke', '#999999')
        .attr('stroke-width', '3px')
        .attr('stroke-opacity', function(d) {
            return d.weight;
        });

    var node = svg.append('g')
        .attr('class', 'nodes')
        .selectAll('circle')
        .data(graph.nodes)
        .enter().append('circle')
        .attr('r', 10)
        .attr('fill', function(d) { return color(d.id); })
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    node.append('title')
        .text(function(d) { return d.id; });

    simulation
        .nodes(graph.nodes)
        .on('tick', ticked);

    simulation.force('link')
        .links(graph.links);

    function ticked() {
        link
            .attr('x1', function(d) { return d.source.x; })
            .attr('y1', function(d) { return d.source.y; })
            .attr('x2', function(d) { return d.target.x; })
            .attr('y2', function(d) { return d.target.y; });

        node
            .attr('cx', function(d) { return d.x; })
            .attr('cy', function(d) { return d.y; });
    }
    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

(function(){
    var wrapperWidth = +d3.select('#canvas-wrapper').style('width').slice(0, -2);
    var graphsPerRow = 4;
    var graphsPerColumn = 2;
    var canvasWidth = wrapperWidth;
    var wrapperHeight = canvasWidth / graphsPerRow * graphsPerColumn;
    var cellWidth = canvasWidth / graphsPerRow;
    d3.select('#canvas-wrapper')
        .style('height', wrapperHeight + 'px')
        .style('border', '1px solid #999999');

    d3.select('#canvas')
        .attr('width', canvasWidth);

    d3.json('graph.json', function(data) {
        var len = data.length;
        var maxRowCnt = Math.ceil(len / graphsPerRow);
        d3.select('#canvas')
            .attr('height', maxRowCnt * cellWidth);
        for (var i = 0; i < data.length; i++) {
            var graph = data[i];
            var config = {}
            config.cntPerRow = graphsPerRow;
            config.cntPerColumn = graphsPerColumn;
            config.index = i;
            config.cellWidth = cellWidth;
            drawGraph(graph, config);
        }
    });
})();

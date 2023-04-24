import * as d3 from 'd3'

export default function densityChart(){
    var chart = d3.select('#densityChart')
    var data = [[1, 2], [2, 4], [3, 6]]
    
    chart.append("circle")
    chart.attr("cx", 3)
}
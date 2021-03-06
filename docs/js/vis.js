//# dc.js Getting Started and How-To Guide
'use strict';

/* jshint globalstrict: true */
/* global dc,d3,crossfilter */

// ### Create Chart Objects

// Create chart objects associated with the container elements identified by the css selector.
// Note: It is often a good idea to have these objects accessible at the global scope so that they can be modified or
// filtered by other page controls.
var gainOrLossChart = dc.pieChart('#gain-loss-chart');
var volumeChart = dc.barChart('#monthly-volume-chart');
var dayOfWeekChart = dc.rowChart('#day-of-week-chart');
var timeOfDayChart = dc.rowChart('#time-of-day-chart');
var nasdaqTable = dc.dataTable('.dc-data-table');
var composite = dc.compositeChart("#test_composed");
var differenceChart = dc.lineChart('#difference-chart');
var boxMT = dc.numberDisplay("#mt-number-box")
var boxML = dc.numberDisplay("#ml-number-box")
var boxPM = dc.numberDisplay("#pm-number-box")

var charts = [
    gainOrLossChart,
    differenceChart,
    composite,
    dayOfWeekChart,
    timeOfDayChart,
    volumeChart];

// ### Anchor Div for Charts

window.filter = function(filters) {
    filters.forEach(function(d, i) { charts[i].filter(d); });
    dc.renderAll();
  };

  window.reset = function(i) {
    charts[i].filter(null);
    dc.renderAll();
  };
//### Load your data
function update_models(){
    var ml_check = document.getElementById("mlcheck").checked;
    var mt_check = document.getElementById("mtcheck").checked;
    var pm_check = document.getElementById("pmcheck").checked;


    var e = document.getElementById("selectGraph");
    var strUser = e.options[e.selectedIndex].value;
    d3.csv('data.csv').then(function (data) { 
        //define filter for links in text

        var forceMLPlot = false
        var data = data.map(function(d) {
          if (ml_check) {var ml_map = d.ml_occupancy} else {var ml_map = 0}
          if (mt_check) {var mt_map = d.mt_occupancy} else {var mt_map = 0}
          if (pm_check) {var pm_map = d.pm_occupancy} else {var pm_occupancy = 0}
          var output = {datetime: d.datetime, ml_occupancy: ml_map,mt_occupancy: mt_map,pm_occupancy: pm_map}
          return output
        });

        // hide plot when crowdsourcing is off
        if (mt_check == false){
             document.getElementById('difference-chart').setAttribute("style", "display:none;");
        }
        else{
            document.getElementById('difference-chart').setAttribute("style", "display:;");
        }

        // Since its a csv file we need to format the data a bit.
        var dateFormatSpecifier = '%m/%d/%Y %H:%M';
        var dateFormat = d3.timeFormat(dateFormatSpecifier);
        var dateParse = d3.timeParse("%m/%d/%Y %H:%M");
        var numberFormat = d3.format('.2f');

        data.forEach(function (d) {
            d.dd = dateParse(d.datetime);
            d.day = d3.timeDay(d.dd); // pre-calculate month for better performance
            d.day = d3.timeHour(d.dd); // pre-calculate month for better performance
            d.pm_occupancy = +d.pm_occupancy; 
            d.mt_occupancy = +d.mt_occupancy; 
            d.ml_occupancy = +d.ml_occupancy;
        });

        //See the [crossfilter API](https://github.com/square/crossfilter/wiki/API-Reference) for reference.
        var ndx = crossfilter(data);
        var all = ndx.groupAll();

        // ## Dimensions
        var dailyDimension = ndx.dimension(function (d) { return d3.timeDay(d.dd);});
        var dateDimension = ndx.dimension(function (d) {return d.dd;});
        var moveDays = ndx.dimension(function (d) { return d.day;});
        var gainOrLoss = ndx.dimension(function (d) {
            return (24 > (d.mt_occupancy  || d.ml_occupancy  || d.pm_occupancy)) ? 'underutilized' : 'overutilized';
        });
        var dayOfWeek = ndx.dimension(function (d) {
            var day = d.dd.getDay();
            var name = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            return day + '.' + name[day];
        });

        var timeOfDay = ndx.dimension(function (d) {
            var time = d.dd.getHours();
            return time;
        });

         var diffDimension_pm = ndx.dimension(function (d) {
            var day = d.dd.getDay();
            if(day > 0){ //not sunday
                var time = d.dd.getHours();
                return time;
            }
            else{
                return -10000;
            }
        });

        var diffDimension_ml = ndx.dimension(function (d) {
            var day = d.dd.getDay();
            if(day > 0){ //not sunday
                var time = d.dd.getHours();
                return time;
            }
            else{
                return -10000;
            }
        });

        function reduceMLAdd(p, v) {
          ++p.count;
          p.total += (v.ml_occupancy - v.mt_occupancy);
          return p;
        }

        function reduceMLRemove(p, v) {
          --p.count;
          p.total -= (v.ml_occupancy - v.mt_occupancy);
          return p;
        }

        function reduceMLInitial() {
          return {count: 0, total: 0};
        }

        function remove_small_bins(source_group, lower_bound) {
            return {
                all:function () {
                    return source_group.all().filter(function(d) {
                        return d.value > lower_bound;
                    });
                }
            };
        }
         function reduceDiffAdd(p, v) {
                ++p.count;
                p.total += (v.pm_occupancy - v.mt_occupancy);
                if (p.count == 0) {
                    p.average = 0;
                } else {
                    p.average = p.total / p.count;
                };
                return p;
            }
            function reduceDiffRemove(p, v) {
                --p.count;
                p.total -= (v.pm_occupancy - v.mt_occupancy);
                if (p.count == 0) {
                    p.average = 0;
                } else {
                    p.average = p.total / p.count;
                };
                return p;
            }
            function reduceDiffInitial() {
                return {
                    count: 0,
                    total: 0,
                    average: 0
                };
        }
        var average = function(d) {return d.n ? d.tot / d.n : 0;};
        // ## Groups
        var volumeByDayGroup = moveDays.group().reduceSum(function (d) {
            return (d.pm_occupancy + d.mt_occupancy + d.ml_occupancy)/3;
        });
        var gainOrLossGroup = gainOrLoss.group();
        var dayOfWeekGroup = dayOfWeek.group();
        var timeOfDayGroup = timeOfDay.group();   
        var mt_group = dateDimension.group().reduceSum(function (d) {return d.mt_occupancy;})
        var pm_group  = dateDimension.group().reduceSum(function (d) {return d.pm_occupancy;});
        var ml_group  = dateDimension.group().reduceSum(function (d) {return d.ml_occupancy;});
        var pm_diff_group = diffDimension_pm.group().reduce(reduceDiffAdd, reduceDiffRemove, reduceDiffInitial);
        var ml_diff_group  = diffDimension_ml.group().reduce(reduceMLAdd, reduceMLRemove, reduceMLInitial);

        // # Calculate total average Occupancy
        var mt_utilization_group = ndx.groupAll()
                                        .reduce( function (p, v) {++p.n;
                                                                    p.tot += (v.mt_occupancy / 31.0);
                                                                    return p;},
                                                function (p, v) {--p.n;
                                                                    p.tot -= (v.mt_occupancy / 31.0);
                                                                    return p;},
                                                function () { return {n:0,tot:0}; });
        var ml_utilization_group = ndx.groupAll()
                                        .reduce( function (p, v) {if(v.ml_occupancy!=0){++p.n;} //filter out
                                                                    p.tot += (v.ml_occupancy / 31.0);
                                                                    return p;},
                                                function (p, v) {if(v.ml_occupancy!=0){--p.n;}
                                                                    p.tot -= (v.ml_occupancy / 31.0);
                                                                    return p;},
                                                function () { return {n:0,tot:0}; });
        var pm_utilization_group = ndx.groupAll()
                                        .reduce( function (p, v) {++p.n;
                                                                    p.tot += (v.pm_occupancy / 31.0);
                                                                    return p;},
                                                function (p, v) {--p.n;
                                                                    p.tot -= (v.pm_occupancy / 31.0);
                                                                    return p;},
                                                function () { return {n:0,tot:0}; });
       
       function remove_empty_bins(source_group) {
            return {
                all:function () {
                    return source_group.all().filter(function(d) {
                        return d.value != 0;
                    });
                }
            };
        }

        var filtered_ml_group = remove_empty_bins(ml_diff_group) // or filter_bins, or whatever

        // # Pie Chart
        gainOrLossChart // dc.pieChart('#gain-loss-chart', 'chartGroup')
            .width(180)
            .height(180)
            .radius(80)
            .dimension(gainOrLoss)
            .colors(d3.scaleOrdinal().range([ '#9ecae1', '#6baed6']))
            .group(gainOrLossGroup)
            .label(function (d) {
                if (gainOrLossChart.hasFilter() && !gainOrLossChart.hasFilter(d.key)) {
                    return d.key + '(0%)';
                }
                var label = d.key;
                if (all.value()) {
                    label += '(' + Math.floor(d.value / all.value() * 100) + '%)';
                }
                return label;
            });

        // # Difference Chart
        if(strUser=="pm"){
        document.getElementById('parkmobilelabel').innerHTML = 'Avg Compliance per Hour';
        differenceChart
            .margins({top: 20, right: 50, bottom: 25, left: 15})
            .width(400)
            .height(200)
            .renderArea(true)
            .x(d3.scaleLinear().domain([8,19]))
            .valueAccessor(function(p) { return p.value.average; })
            .yAxisLabel('')
            .elasticY(true)
            .elasticX(false)
            .dimension(diffDimension_pm)
            .colors('#f0ad4e')
            .group(pm_diff_group, "Park Mobile")
            .brushOn(true);
        }
        else {
        differenceChart.filterAll();dc.redrawAll();
        document.getElementById('parkmobilelabel').innerHTML = 'MAE over Time';
        differenceChart
            .margins({top: 20, right: 50, bottom: 25, left: 15})
            .width(400)
            .height(200)
            .renderArea(true)
            .x(d3.scaleLinear().domain([6,19]))
            .y(d3.scaleLinear().domain([6,19]))
            .valueAccessor(function(p) { return p.value.total; })
            .elasticX(false)
            .elasticY(true)
            .dimension(diffDimension_ml)
            .colors('#5bc0de')
            .group(filtered_ml_group)
            .brushOn(true);
        dc.renderAll();
        }

        boxMT
            .formatNumber(d3.format("0.0%"))
            .valueAccessor(average)
            .group(mt_utilization_group);
        boxML
            .formatNumber(d3.format("0.0%"))
            .valueAccessor(average)
            .group(ml_utilization_group);
        boxPM
            .formatNumber(d3.format("0.0%"))
            .valueAccessor(average)
            .group(pm_utilization_group);

        dayOfWeekChart /* dc.rowChart('#day-of-week-chart', 'chartGroup') */
            .width(70)
            .height(300)
            .margins({top: 20, left: 10, right: 10, bottom: 20})
            .group(dayOfWeekGroup)
            .dimension(dayOfWeek)
            // Assign colors to each value in the x scale domain
            .ordinalColors(['#3182bd', '#3182bd','#6baed6','#6baed6','#6baed6','#6baed6','#6baed6'])
            .label(function (d) {
                return d.key.split('.')[1];
            })
            // Title sets the row text
            .title(function (d) {
                return d.value;
            })
            .elasticX(true)
            .xAxis().ticks(2);

        timeOfDayChart /* dc.rowChart('#day-of-week-chart', 'chartGroup') */
            .width(60)
            .height(300)
            .margins({top: 20, left: 2, right: 6, bottom: 20})
            .group(timeOfDayGroup)
            .ordinalColors(['#6baed6'])
            .dimension(timeOfDay)
            // Title sets the row text
            .elasticX(true)
            .xAxis().ticks(3);

        composite
            .width(650)
            .height(300)
            .transitionDuration(800)
            .x(d3.scaleTime().domain(d3.extent(data, function(d) { return d.dd; })))
            .yAxisLabel("Occupancy")
            .xUnits(d3.timeDays)
            .elasticY(true)
            .legend(dc.legend().x(90).y(20).itemHeight(10).gap(5))
            .renderHorizontalGridLines(true)
            .margins({top: 20, right: 10, bottom: 25, left: 35})
            .rangeChart(volumeChart)
            .compose([
                dc.lineChart(composite)
                    .dimension(dateDimension)
                    .colors('#5cb85c')
                    .group(mt_group, "Crowdsourcing"),
                dc.lineChart(composite)
                    .dimension(dateDimension)
                    .colors('#f0ad4e')
                    .group(pm_group, "Park Mobile"),
                dc.lineChart(composite)
                    .dimension(dateDimension)
                    .colors('#5bc0de')
                    .group(ml_group, "Machine Learning")
                ])
            .brushOn(false)

        composite.xAxis().ticks(10)

        // # Bar Chart
        volumeChart.width(790) // dc.barChart('#monthly-volume-chart', 'chartGroup');
            .height(40)
            .margins({top: 0, right: 50, bottom: 20, left: 40})
            .dimension(moveDays)
            .group(volumeByDayGroup)
            .centerBar(true)
            .gap(95)
            .colors(['#6baed6'])
            .x(d3.scaleTime().domain(d3.extent(data, function(d) { return d.day; })))
            .round(d3.timeDay.round)
            .alwaysUseRounding(true)
            .xUnits(d3.timeDays);

        //#### Data Table

        // Create a data table widget and use the given css selector as anchor. You can also specify
        // an optional chart group for this chart to be scoped within. When a chart belongs
        // to a specific group then any interaction with such chart will only trigger redraw
        // on other charts within the same chart group.
        // <br>API: [Data Table Widget](https://github.com/dc-js/dc.js/blob/master/web/docs/api-latest.md#data-table-widget)
        //
        // You can statically define the headers like in
        // ```
        // or do it programmatically using `.columns()`.

        nasdaqTable // dc.dataTable('.dc-data-table', 'chartGroup') 
            .dimension(dateDimension)
            // Data table does not use crossfilter group but rather a closure
            // as a grouping function
            .group(function (d) {
                var format = d3.format('02d');
                return d.dd + '/' + format((d.dd.getMonth() + 1));
            })
            // (_optional_) max number of records to be shown, `default = 25`
            .size(10)
            // There are several ways to specify the columns; see the data-table documentation.
            // This code demonstrates generating the column header automatically based on the columns.
            .columns(['date','pm_occupancy', 'mt_occupancy', 'ml_occupancy'])
            // (_optional_) sort using the given field, `default = function(d){return d;}`
            .sortBy(function (d) {
                return d.dd;
            })
            // (_optional_) sort order, `default = d3.ascending`
            .order(d3.ascending)
            // (_optional_) custom renderlet to post-process chart using [D3](http://d3js.org)
            .on('renderlet', function (table) {
                table.selectAll('.dc-table-group').classed('info', true);
            });

        //#### Rendering

        //simply call `.renderAll()` to render all charts on the page
        dc.renderAll();     
        });
    }

    update_models();
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
var lfckv = document.getElementById("mlcheck").checked;
                alert(lfckv);
// ### Anchor Div for Charts

//### Load your data

d3.csv('sample_output.csv').then(function (data) {
    var data = data.map(function(d) {
      return {
        datetime: d.datetime,
        mt_occupancy: d.mt_occupancy,
        pm_occupancy: d.pm_occupancy,
        ml_occupancy: d.ml_occupancy,
      }
    });

    // Since its a csv file we need to format the data a bit.
    var dateFormatSpecifier = '%m/%d/%Y %H:%M';
    var dateFormat = d3.timeFormat(dateFormatSpecifier);
    var dateParse = d3.timeParse("%m/%d/%Y %H:%M");
    var numberFormat = d3.format('.2f');

    data.forEach(function (d) {
        d.dd = dateParse(d.datetime);
        d.day = d3.timeDay(d.dd); // pre-calculate month for better performance
        d.pm_occupancy = +d.pm_occupancy; 
        d.mt_occupancy = +d.mt_occupancy; 
        d.ml_occupancy = +d.ml_occupancy;
    });


    //See the [crossfilter API](https://github.com/square/crossfilter/wiki/API-Reference) for reference.
    var ndx = crossfilter(data);
    var all = ndx.groupAll();

    // Dimension by year
    var dailyDimension = ndx.dimension(function (d) {
        return d3.timeDay(d.dd);
    });

    // Dimension by full date
    var dateDimension = ndx.dimension(function (d) {return d.dd;});

    // Dimension by month
    var moveDays = ndx.dimension(function (d) { return d.day;});

    // Group by total volume within move, and scale down result
    var volumeByDayGroup = moveDays.group().reduceSum(function (d) {
        return (d.pm_occupancy + d.mt_occupancy + d.ml_occupancy)/3;
    });

    // Create categorical dimension
    var gainOrLoss = ndx.dimension(function (d) {
        return 24 > d.mt_occupancy ? 'underutilized' : 'overutilized';
    });
    // Produce counts records in the dimension
    var gainOrLossGroup = gainOrLoss.group();

    // Counts per weekday
    var dayOfWeek = ndx.dimension(function (d) {
        var day = d.dd.getDay();
        var name = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        return day + '.' + name[day];
    });
    var dayOfWeekGroup = dayOfWeek.group();

     var timeOfDay = ndx.dimension(function (d) {
        var time = d.dd.getHours();
        return time;
    });
    var timeOfDayGroup = timeOfDay.group();   

    var mt_group = dateDimension.group().reduceSum(function (d) {return d.mt_occupancy;})
    var pm_group  = dateDimension.group().reduceSum(function (d) {return d.pm_occupancy;});
    var ml_group  = dateDimension.group().reduceSum(function (d) {return d.ml_occupancy;});


    composite
        .width(900)
        .height(300)
        .transitionDuration(800)
        .x(d3.scaleTime().domain(d3.extent(data, function(d) { return d.dd; })))
        .yAxisLabel("The Y Axis")
        .xUnits(d3.timeDays)
        .elasticY(true)
        .legend(dc.legend().x(80).y(20).itemHeight(13).gap(5))
        .renderHorizontalGridLines(true)
        .margins({top: 30, right: 50, bottom: 25, left: 40})
        .rangeChart(volumeChart)
        .compose([
            dc.lineChart(composite)
                .dimension(dateDimension)
                .colors('#900c3f')
                .group(mt_group, "Crowdsourcing"),
            dc.lineChart(composite)
                .dimension(dateDimension)
                .colors('#0c3f90')
                .group(pm_group, "Park Mobile"),
            dc.lineChart(composite)
                .dimension(dateDimension)
                .colors('#3f900c')
                .group(ml_group, "Machine Learning")
            ])
        .brushOn(false)
      
    // # Pie Chart
    gainOrLossChart // dc.pieChart('#gain-loss-chart', 'chartGroup')
        .width(180)
        .height(180)
        .radius(80)
        .dimension(gainOrLoss)
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

      dayOfWeekChart /* dc.rowChart('#day-of-week-chart', 'chartGroup') */
        .width(180)
        .height(180)
        .margins({top: 20, left: 10, right: 10, bottom: 20})
        .group(dayOfWeekGroup)
        .dimension(dayOfWeek)
        // Assign colors to each value in the x scale domain
        .ordinalColors(['#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#dadaeb'])
        .label(function (d) {
            return d.key.split('.')[1];
        })
        // Title sets the row text
        .title(function (d) {
            return d.value;
        })
        .elasticX(true)
        .xAxis().ticks(4);

      timeOfDayChart /* dc.rowChart('#day-of-week-chart', 'chartGroup') */
        .width(180)
        .height(300)
        .margins({top: 20, left: 20, right: 10, bottom: 20})
        .group(timeOfDayGroup)
        .dimension(timeOfDay)
        // Title sets the row text
        .elasticX(true)
        .xAxis().ticks(4);

    // # Bar Chart
    volumeChart.width(990) // dc.barChart('#monthly-volume-chart', 'chartGroup');
        .height(40)
        .margins({top: 0, right: 50, bottom: 20, left: 40})
        .dimension(moveDays)
        .group(volumeByDayGroup)
        .centerBar(true)
        .gap(1)
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
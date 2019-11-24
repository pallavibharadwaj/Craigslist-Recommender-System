
function loadHighcharts(data) {
    Highcharts.mapChart('container', {
        chart: {
            renderTo: container,
            map: 'countries/ca/ca-all',
        },
        title: {
            text: ''
        },
        mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },
        colorAxis: {
            min: 0,
            minColor: '#add8e6',
            maxColor: '#ff0000',
            labels: {
                formatter: function () {
                    return this.value;
                }
            }
        },
        series: [{
            data: data,
            name: 'Number of Posts',
            states: {
                hover: {
                    color: '#808080'
                }
            },
            dataLabels: {
                enabled: true,
                format: '{point.name}'
            },
        }],
        xAxis: {
            maxPadding:0
        },
        yAxis: {
            maxPadding: 0
        },
        credits: {
            enabled: false
        }
    });
}

function loadHighcharts2() {
    Highcharts.chart('container2', {
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Monthly Average Temperature'
        },
        subtitle: {
            text: 'Source: WorldClimate.com'
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            title: {
                text: 'Temperature'
            },
            labels: {
                formatter: function () {
                    return this.value + '°';
                }
            }
        },
        tooltip: {
            crosshairs: true,
            shared: true
        },
        plotOptions: {
            spline: {
                marker: {
                    radius: 4,
                    lineColor: '#666666',
                    lineWidth: 1
                }
            }
        },
        series: [{
            name: 'Tokyo',
            marker: {
                symbol: 'square'
            },
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, {
                y: 26.5,
                marker: {
                    symbol: 'url(https://www.highcharts.com/samples/graphics/sun.png)'
                }
            }, 23.3, 18.3, 13.9, 9.6]

        }, {
            name: 'London',
            marker: {
                symbol: 'diamond'
            },
            data: [{
                y: 3.9,
                marker: {
                    symbol: 'url(https://www.highcharts.com/samples/graphics/snow.png)'
                }
            }, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
        }],
        credits: {
            enabled: false
        }

    });
}

$(document).ready(function () 
{
    $.ajax({
        url:"http://localhost:5000/data",
        dataType: 'json',
        headers: {  
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        }, 
        success:function(json){
            loadHighcharts(json['val1']);
        },
        error:function(request, error){
            console.log(error); //Should be removed after dev phase
        }
    });
    $.ajax({
        url:"http://localhost:5000/data",
        dataType: 'json',
        headers: {  
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        }, 
        success:function(){
            loadHighcharts2();
        },
        error:function(request, error){
            console.log(error); //Should be removed after dev phase
        }
    });

});


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

function loadMedianRent(resp) {
    Highcharts.chart('medianrent', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Median Rent(CAD) in popular Canadian cities'
        },
        xAxis: {
            categories: resp['cities']
        },
        yAxis: {
            title: {
                text: 'Median Rent'
            },
        },
        tooltip: {
            crosshairs: true,
            shared: true
        },
        plotOptions: {
            series: {
                allowPointSelect: true
            }
        },
        series: [{
            name:'1 Bedroom',
            data: resp['rent1']
        },{
            name:'2 Bedroom',
            data:resp['rent2']
        },{
            name:'3 Bedroom',
            data:resp['rent3']
        }],
        credits: {
            enabled: false
        }
    });
}


<<<<<<< HEAD
=======

>>>>>>> 5d03d9013bb71dfbfe6011efa38aa2445d0f09df
function loadPetAnimals(data){
    Highcharts.chart('petanimals', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Percentage of listings allowing various pets'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: 'Listings',
        colorByPoint: true,
        data: [{
            name: 'No pets allowed',
            y: data['none'],
            sliced: true,
            selected: true
        }, {
            name: 'Cats',
            y: data['cats']
        }, {
            name: 'Dogs',
            y: data['dogs']
        }, {
            name: 'Both cats and dogs',
            y: data['both']
        }]
    }]
  });
}

<<<<<<< HEAD
function loadWheelchair(data){
    Highcharts.chart('wheelchair', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Percentage of Canada wide listings that have wheelchair accessibility'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: 'Listings',
        colorByPoint: true,
        data: [{
            name: 'No wheelchair access',
            y: data['none'],
            sliced: true,
            selected: true
        }, {
            name: 'Wheelchair access',
            y: data['wheelchair']
        }]
    }]
  });
}


=======
>>>>>>> 5d03d9013bb71dfbfe6011efa38aa2445d0f09df
$(document).ready(function () 
{
    $.ajax({
        url:"http://localhost:5000/chartdata",
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
        url:"http://localhost:5000/chartdata",
        dataType: 'json',
        headers: {  
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        }, 
        success:function(json){
            loadMedianRent(json['medianrent']);
        },
        error:function(request, error){
            console.log(error); //Should be removed after dev phase
        }
    });
    $.ajax({
        url:"http://localhost:5000/chartdata",
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        success:function(json){
            loadPetAnimals(json['petanimals']);
<<<<<<< HEAD
        },
        error:function(request, error){
            console.log(error); //Should be removed after dev phase
        }
    });
    $.ajax({
        url:"http://localhost:5000/chartdata",
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        success:function(json){
            loadWheelchair(json['wheelchair']);
=======
>>>>>>> 5d03d9013bb71dfbfe6011efa38aa2445d0f09df
        },
        error:function(request, error){
            console.log(error); //Should be removed after dev phase
        }
    });
});


function loadHighcharts(data) {
    Highcharts.mapChart('container', {
        chart: {
            renderTo: container,
            map: 'countries/ca/ca-all',
        },
        title: {
            text: 'Heat Map for Number of Posts per Region'
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
    }],
    credits: {
            enabled: false
    }
  });
}

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
    credits: {
            enabled: false
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

function loadHeatMap(data) {
    Highcharts.mapChart('heatmap2', {
        chart: {
            renderTo: heatmap2,
            map: 'countries/ca/ca-all',
        },
        title: {
            text: 'Heat Map for Median Price per Region'
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
            name: 'Median Price',
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

function loadBoxplot(resp) {
    Highcharts.chart('boxplot', {

    chart: {
        type: 'boxplot'
    },

    title: {
        text: 'Box Plot for Rent distribution'
    },

    legend: {
        enabled: false
    },

    xAxis: {
        categories: resp['regions'] ,

        title: {
            text: 'Province / Territory'
        }
    },

    yAxis: {
        floor : 0,
        title: {
            text: 'Price in CAD'
        },
    },

    series: [{
        name: 'Rent Distribution',

        data : resp['val'],

        tooltip: {
            headerFormat: '<em>Province/Territory : {point.key}</em><br/>'
        }
    }],
        credits: {
            enabled: false
        }

  });
}

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
            loadHighcharts(json['heatmap_posts']);
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
            loadHeatMap(json['heatmap_price']);
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
            loadBoxplot(json['boxplot']);
        },
        error:function(request, error){
            console.log(error); //Should be removed after dev phase
        }
    });
});

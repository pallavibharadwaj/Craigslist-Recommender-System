
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

function loadSpline(resp) {
    Highcharts.chart('spline', {
    chart: {
        type: 'areaspline'
    },
    title: {
        text: 'Posts per day of the week'
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 150,
        y: 100,
        floating: true,
        borderWidth: 1,
        backgroundColor:
            Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF'
    },
    xAxis: {
        categories: [
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday'
        ]
    },
    yAxis: {
        title: {
            text: 'Number of posts'
        }
    },
    tooltip: {
        shared: true,
        valueSuffix: ' posts'
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        areaspline: {
            fillOpacity: 0.5
        }
    },
    series: [{
        name: resp[0][0],
        data: resp[0][1],
        visible : false
    }, {
        name: resp[1][0],
        data: resp[1][1],
        visible : false
    }, {
        name: resp[2][0],
        data: resp[2][1],
        visible : false
    }, {
        name: resp[3][0],
        data: resp[3][1],
        visible : false
    }, {
        name: resp[4][0],
        data: resp[4][1],
        visible : false
    }, {
        name: resp[5][0],
        data: resp[5][1],
        visible : false
    }, {
        name: resp[6][0],
        data: resp[6][1],
        visible : true
    }, {
        name: resp[7][0],
        data: resp[7][1],
        visible : true
    }, {
        name: resp[8][0],
        data: resp[8][1],
        visible : false
    }, {
        name: resp[9][0],
        data: resp[9][1],
        visible : false
    }, {
        name: resp[10][0],
        data: resp[10][1],
        visible : false
    }, {
        name: resp[11][0],
        data: resp[11][1],
        visible : true
    }]
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
            loadSpline(json['spline']);
            loadBoxplot(json['boxplot']);
            loadMedianRent(json['medianrent']);
            loadPetAnimals(json['petanimals']);
            loadHeatMap(json['heatmap_price']);
            loadWheelchair(json['wheelchair']);
        },
        error:function(request, error){
            console.log(error); //Should be removed after dev phase
        }
    });
});



//create a drawing context on the canvas
var $element = document.getElementById("windspeed");

if ($element !== null){
    var windspeed_analysisChart;
    var windspeed_analysis_ctx = $element.getContext("2d"),
        windspeed_data = {},
        windspeed_analysis_labels = ["speed",],
        windspeed_analysis_borderColor = {
            'speed': 'rgba(0, 90, 255, 1)',
        },
        windspeed_analysis_backgroundColor = {
            'speed': 'rgba(0, 90, 255, .6)',
        };

    // using jQuery ajax method get data from the external file. ( while using react you will do it differently)
    var jsonData = $.ajax({
        url: 'wind.json',
        dataType: 'json',
    }).done(function(results)
    {
        processedData = windspeed_analysisprocessData(results);
        var pointerImage = new Image(10, 20);
        pointerImage.src="resources/arrow_up.svg"
        var presets = window.chartColors;
        windspeed_data = {
            labels: processedData.x_labels,
            datasets: [
                {
                    label: "wind speed",
                    data: processedData.data,
                    borderColor: windspeed_analysis_borderColor["speed"],
                    backgroundColor: windspeed_analysis_backgroundColor["speed"],
                    fill: true,

                    pointStyle: pointerImage,
                    pointRadius: 30,
                    pointRotation: function(ctx) {

                        // compute angle based on whatever is your use case:
                        return ctx.dataset.data[ctx.dataIndex].d;
                    }
                }
            ]
        };

        var options = {
            maintainAspectRatio: false,
            responsive: true,
            spanGaps: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Wind Speed for ' + results['datetime'].slice(0,10)
                },
            },
            scales: {
                x: {
                    display: true,
                    type: 'time',
                    time: {
                        //parser: 'DD-MM-YYYY HH:mm',
                        parser: 'YYYY-MM-DD HH:mm',
                        tooltipFormat: 'HH:mm DD/MM/YYYY',
                        unit: 'hour',
                        unitStepSize: 1,
                        displayFormats: {
                            'day': 'DD/MM/YYYY',

                            'hour': 'DD-MM HH:mm',
                            'minute': 'HH:mm',
                        }
                    },


                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'µm/m³'
                    }
                }
            },
        };

        windspeed_analysisChart = new Chart(windspeed_analysis_ctx, {
            type: 'line',
            data: windspeed_data,
            options: options
        });

    });

}

// translates the data json into an array that can be processed by Chart.js
var windspeed_analysisprocessData = function(jsonData)
{
    //var locale = "en-us";
    myformat = Intl.NumberFormat('it-it', { minimumIntegerDigits: 2 })

    var x_labels = Object.keys(jsonData["data"]).map(function(item) {
        return new Date(item);
    }).sort((a, b) => a - b);
    console.log(x_labels)
    var dataSet = [],
        isodata = '';

    // a data set for speed

    for (const [date_time, row_data] of Object.entries(jsonData["data"])) {

    //for (var j = 0; j < x_labels.length; j++) {
    //    date_string = x_labels[j].getFullYear()+'-'+myformat.format(x_labels[j].getMonth()+1)+'-'+myformat.format(x_labels[j].getDate())+' '+myformat.format(x_labels[j].getHours())+':'+myformat.format(x_labels[j].getMinutes())+':'+myformat.format(x_labels[j].getSeconds())

        dataSet.push({
            x: date_time,
            y: row_data["speed"],
            d: row_data["direction"],
        })

    }
    return {
        labels: windspeed_analysis_labels,
        x_labels: x_labels,
        data: dataSet,
        borderColor: windspeed_analysis_borderColor,
        backgroundColor: windspeed_analysis_backgroundColor
    }
};

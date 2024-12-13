const { Legend } = require("chart.js")

var labels, values

function init(_labels, _values) {
    labels = _labels
    values = _values
    drawChart()

    document.getElementById('return-button').addEventListener('click', function() {
        window.location.assign('/')
    })
}

function drawChart() {
    const ctx = document.getElementById('evolution-chart')
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'data1',
                data: values,
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    })
}
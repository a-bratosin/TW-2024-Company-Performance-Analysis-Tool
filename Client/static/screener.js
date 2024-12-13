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
                label: 'Turnover',
                data: values,
                segment: {
                    borderDash: ctx => (ctx.p0.label > 2023 || ctx.p1.label > 2023 ? [6, 6] : undefined)
                },
                spanGaps: true
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
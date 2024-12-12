var labels, values

function init(_labels, _values) {
    labels = _labels
    values = _values
    drawChart()
}

function drawChart() {
    const ctx = document.getElementById('evolution-chart')
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: values,
            }]
        }
    })
}
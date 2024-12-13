let button = document.getElementById('search-button')
let field = document.getElementById('search-field')
button.addEventListener('click', function () {
    let value = field.value
    if (!value.trim().length) {
        return false
    }
    let route = 'predict/'.concat(value)
    window.location.assign(route)
})
let button = document.getElementById('search_button')
let field = document.getElementById('search_field')
button.addEventListener('click', function () {
    let baseAddress = window.location.pathname
    let route = 'post/'.concat(field.value)
    route = baseAddress.concat(route)
    window.alert(route)
    window.location.assign(route)
})
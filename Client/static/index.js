let button = document.getElementById('search_button')
let field = document.getElementById('search_field')
button.addEventListener('click', function () {
    let route = 'post/'.concat(field.value)
    window.location.assign(route)
})
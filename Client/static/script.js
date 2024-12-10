let button = document.querySelector('#search_company')
button.addEventListener('click', function () {
    console.log("Click")
    fetch('http://localhost:3000/search_company')
        .then(response => response.json())
        .then(data => console.log(data))
})
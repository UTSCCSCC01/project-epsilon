function filter() {
    /*const element = document.getElementById("filter");
    const checkValue = element.options[element.selectedIndex].value;
    const checkText = element.options[element.selectedIndex].text;

    element.addEventListener("change", (e) => {
    const value = e.target.value;
    const text = element.options[element.selectedIndex].text;

    if (value) {
    document.getElementById("pick").textContent = `Value Selected: ${value}`;
    document.getElementsByClassName(`${value}`)[0].style.visibility='hidden';
    } else {
    document.getElementById("pick").textContent = "";
    }
    })*/
    console.log(services);

    for (var key in services) {
            var title = services[key][3];
            var desc = services[key][4];
            var price = services[key][5];
            var link = services[key][6];
            var badge = document.createElement('div');
            badge.className = 'jumbotron';
            badge.innerHTML =
                '<h1 class="display-4">'+ title +'</h1>' +
                '<p class="lead">' + desc + '</p>' +
                '<hr class="my-4">' + link + '</a>' +
                '<p>'+ 'Price: ' + price + '</p>' +
                '<br>' +
                '<p class="lead">' +
                '<a class="btn btn-primary main-button" href='+ link +' target=”_blank” role="button">Learn' +
                'more' + '</a>';
            document.getElementById('services').appendChild(badge);
    }
}


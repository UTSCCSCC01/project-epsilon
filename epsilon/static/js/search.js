// currently no import works
// import React  from 'react';
// import ReactDOM from 'react-dom';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import Card from "react-bootstrap/Card";

function render_data() {
    for (var key in company_data) {
        for (var i = 0; i < company_data[key].length; i++) {
            var title = company_data[key][i].name;
            var desc = company_data[key][i].description;
            var tid = company_data[key][i].tid;
            var link = "http://127.0.0.1:5000/company/" + tid;
            var badge = document.createElement('div');
            badge.className = 'search-result-box card-box';
            badge.innerHTML =
                '<div class="search-item">' +
                '<h4 class="search-title">' + title + '</h4>' +
                '<div class="font-13 text-success mb-3">' +
                '<a class="link" href='+ link +'>' + link + '</a>' +
                '</div>' +
                '<p class="mb-0 text-muted">' + desc + '</p>' +
                '</div>';
            document.getElementById('search-data').appendChild(badge);
        }
    }
}

function render_error() {
        var badge = document.createElement('div');
        badge.className = 'search-result-box card-box';
        badge.innerHTML = '<p class="error">' + error.message + '</p>';
        document.getElementById('error-data').appendChild(badge);
}
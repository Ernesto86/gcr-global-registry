'use strict';
const units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
const loadingUi = document.getElementById('load-content');
document.addEventListener("DOMContentLoaded", function (e) {
    e.preventDefault();
    loadingUi.style.display = 'none'
});

const mFetch = async (url, data, method = 'POST', loading = null) => {
    let options = {
        method: method,
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    }
    if (method === 'GET') {
        url += '?' + (new URLSearchParams(data)).toString();
    } else {
        options.body = data instanceof FormData ? data : JSON.stringify(data)
    }
    loadingUi.style.display = loading;
    const response = await fetch(url, options);
    loadingUi.style.display = 'none'
    const status = response.status;
    const responseJson = await response.json();
    return [status, responseJson];
};

function niceBytes(x) {
    let l = 0, n = parseInt(x, 10) || 0;
    while (n >= 1024 && ++l) {
        n = n / 1024;
    }
    //include a decimal point and a tenths-place digit if presenting
    //less than ten of KB or greater units
    return (n.toFixed(n < 10 && l > 0 ? 1 : 0) + ' ' + units[l]);
}

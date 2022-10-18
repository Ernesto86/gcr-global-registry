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
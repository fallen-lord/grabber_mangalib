someCode = """

function parseCookies() {
    var cookies = document.cookie.split(';');
    var cookieObject = {};

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim().split('=');
        var cookieName = cookie[0];
        var cookieValue = cookie[1];
        cookieObject[cookieName] = cookieValue;
    }

    return cookieObject;
}



function list_manga(page_number) {

    var xhr = new XMLHttpRequest();
    var url = "https://mangalib.me/api/list";
    var jsonData = {"sort":"rate","dir":"desc","page":page_number,"types":["6"],"site_id":"1","type":"manga","caution_list":["Отсутствует","16+","18+"]};

    xhr.open("POST", url, true);

    var jsonDataString = JSON.stringify(jsonData);

    // Set the appropriate headers
    var cookiesObject = parseCookies();
    xhr.setRequestHeader("Accept", "application/json, text/plain, */*")
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    xhr.setRequestHeader("X-Xsrf-Token", cookiesObject['XSRF-TOKEN'].replace("%3D", "="));
    xhr.setRequestHeader("X-Requested-With", 'XMLHttpRequest');
    xhr.setRequestHeader("X-Csrf-Token", window._PushData.csrfToken);


    // Set cookies as headers
    // xhr.setRequestHeader("Cookie", "cookie1=value1; cookie2=value2");


    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                // Successful response
                //console.log("Response:", xhr.responseText);
                document.rrd = JSON.parse(xhr.response);
            } else {
                // Error handling for non-200 status codes
                console.error("Error:", xhr.status, xhr.statusText);
            }
        }
    };

    xhr.send(jsonDataString);

}

"""

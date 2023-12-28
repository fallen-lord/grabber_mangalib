fetch_list_manga = """

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
    var jsonData = {"sort":"rate","dir":"desc","page":page_number,"types":["1"],"site_id":"1","type":"manga","caution_list":["Отсутствует","16+","18+"]};

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


fetch_chapter = """

function fetchData(url) {

    document.next_page = "";
    
    var xhr = new XMLHttpRequest();
    //var url = "https://mangalib.me/wo-laopo-shi-mowang-darren/v1/c437";


    xhr.open("GET", url, false); // Note: The third parameter is set to false for synchronous
        
    xhr.send();
    if (xhr.readyState == 4 && xhr.status == 200) {
        // Successful response
        document.next_page = xhr.response;
    } else {
        // Error handling for non-200 status codes
        var error = new Error(`HTTP error! Status: ${xhr.status}`);
        throw error;
}
};

"""


asyncJS = """

async function ignoreErrors(allResults) {
  return allResults.filter(result => Array.isArray(result));
}

async function getPageHTML(link) {
  try {
    pageNumber = link[0]
    url = link[1]
    const response = await fetch(url);

    const result = await response.text();
     // console.log(pageNumber);
      if (!response.ok) {
      return null;
    }

    return [link[0], result];
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

async function resultLinks(links, asyncFunc) {
  const tasks = links.map((link) => asyncFunc(link));
  const results = await Promise.allSettled(tasks);

  return results.map(result => result.status === 'fulfilled' ? result.value : null);
}

async function mainAsync(links, asyncFunc, tryCount = 5) {
  let allResults = [];
  links = links.map((link, i) => [i, link]);

  for (let i = 0; i < tryCount; i++) {
    const results = await resultLinks(links, asyncFunc);
    const errorLinks = [];
    allResults = allResults.concat(results.filter(result => result !== null));
    //allResults = allResults.concat(results);

    for (let j = 0; j < results.length; j++) {
      if (results[j] === null) {
        errorLinks.push(links[j]);
      }
    }

      //console.log(allResults);

    if (errorLinks.length === 0) {
      break;
    }

    links = errorLinks;
      //console.log(allResults);

    if (tryCount - i === 1) {
      console.log('Asynchronous error occurred');
     // console.log(results);
    }
  }
    //console.log(allResults);
  allResults = ignoreErrors(allResults);

  //allResults = allResults.sort();
  return allResults;
}

async function main(links, asyncFunc = getPageHTML, tryCount = 5) {
  return await mainAsync(links, asyncFunc, tryCount);
}

document.async_pages = null;


"""


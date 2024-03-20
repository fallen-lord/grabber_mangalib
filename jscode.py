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


function top_manga_list(page_number) {

    var xhr = new XMLHttpRequest();
    var url = "https://mangalib.me/api/list";
    var jsonData = {"sort":"rating_score",
    "dir":"desc",
    "page":page_number,
    "site_id":"1",
    "type":"manga",
    "caution_list":["Отсутствует","16+","18+"]};

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

document.rrd = undefined;


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


async_worker_in_js_format = """

async function filtering_to_unique(results) {
    let uniqueTuplesDict = {};

    for (let [idx, val] of results) {
        if (!(idx in uniqueTuplesDict) || val !== null) {
            uniqueTuplesDict[idx] = [idx, val];
        }
    }

    let uniqueTuples = Object.values(uniqueTuplesDict);
    let uniqueList = uniqueTuples.map(t => t[1]);
    return uniqueList;
}

function filtering_type(results, valueType, toType = true) {
    let keyFunc;
    if (toType) {
        keyFunc = result => typeof result === valueType;
    } else {
        keyFunc = result => typeof result[1] !== valueType;
    }
    return results.filter(keyFunc);
}

async function result_links(links, asyncFunc) {
    let tasks = links.map(link => asyncFunc(link[1]));
    let results = await Promise.allSettled(tasks);
    return results.map(result => result.value);
}

async function async_loop(links, asyncFunc, tryCount, printErrorLinks, ignoreError, valueType) {
    let allResults = [];
    let tc = 0;

    for (let i = 0; i < tryCount; i++) {
        let results = await result_links(links, asyncFunc);
        allResults.push(...results.map((result, j) => [links[j][0], result]));

        let errorLinks = links.filter((link, j) => !(results[j] instanceof Object));

        if (errorLinks.length === 0) {
            break;
        }

        links = errorLinks;

        if (printErrorLinks) {
            console.log(links);
        }
        console.log(i, links);
        tc = i;
    }

    if (tryCount - 1 === tc && !ignoreError) {
        allResults = filtering_type(allResults, valueType, false);
        console.log(links, tryCount, tc, tryCount - 1 === tc, !ignoreError, tryCount - 1 === tc && !ignoreError);
        throw new Error("An error occurred during asynchronous execution");
    }

    return allResults;
}

async function process_links(links, asyncFunc, tryCount = 10, returnResults = true, ignoreError = false, valueType = null, onlySuccessfulResults = false, printErrorLinks = false) {
    if (!Array.isArray(links)) {
        [links, asyncFunc] = [asyncFunc, links];
    }

    tryCount = 10;
    //console.log(tryCount, "ddddddddddddddddddddddd");
    links = links.map((link, i) => [i, link]);
    let allResults = await async_loop(links, asyncFunc, tryCount, printErrorLinks, ignoreError, valueType);

    if (!returnResults) {
        return;
    }

    allResults.sort((a, b) => a[0] - b[0]);
    allResults = await filtering_to_unique(allResults);

    if (onlySuccessfulResults) {
        allResults = filtering_type(allResults, valueType);
    }

    document.all_results = allResults;
    return allResults;
}

async function sync_process_links(...args) {
    document.all_results = undefined;
    return await process_links(...args);
}

"""

manga_short_info = """

async function manga_short_info(anime) {
    const url = "https://mangalib.me/manga-short-info";
    const params = new URLSearchParams({
        id: anime.id,
        slug: anime.slug,
        type: "manga"
    });

    try {
        const response = await fetch(`${url}?${params}`);
        if (response.ok) {
            const result = await response.json();
            return result;
        } else {
            throw new Error(`Failed to fetch manga short info: ${response.status} ${response.statusText}`);
        }
    } catch (error) {
        console.error("Error in manga_short_info:", error);
        throw error;
    }
}

"""


get_page = """

async function get_page(url) {
    try {
        const response = await fetch(url);
        const result = {}
        if (response.ok) {
             result.text = await response.text();
            //const result = await response.json();
            return result;
        } else {
            throw new Error(`Failed to fetch ${url}: ${response.status} ${response.statusText}`);
        }
    } catch (error) {
        console.error("Error in get_page:", error);
        throw error;
    }
}

"""
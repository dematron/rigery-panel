/**
 * Created by kutepoval on 20.05.14.
 */

//create block "location" on the page
function createLocation(parentElement, beforeElement) {
    var buttonAdd = document.createElement('a');
    buttonAdd.className = "button_add";
    buttonAdd.href = "#";
    buttonAdd.setAttribute('onclick', 'createLocation(this.parentNode,this);');
    buttonAdd.innerHTML = "add location here";
    parentElement.insertBefore(buttonAdd, beforeElement);

    var locationBlock = document.getElementById('details_location');
    var newLocationBlock = locationBlock.cloneNode(true);
    parentElement.insertBefore(newLocationBlock, beforeElement);
}

//delete block "location" from the page
function deleteLocation(element) {
    var elements = element.parentNode.getElementsByTagName("details");
    if (elements.length>1) {
        element.previousElementSibling.remove();
        element.remove();
    }
}

//create block "server" on the page
function createServer(parentElement) {
    var serverBlock = document.getElementById('details_server');
    var newServerBlock = serverBlock.cloneNode(true);
    parentElement.appendChild(newServerBlock);
}

//delete block server from the page
function deleteServer(element) {
    var elements = document.getElementsByName("details_server");
    if (elements.length>1) {
        element.remove();
    }
}



function addOptionInclude(parentElement, afterElement) {
    var elementP = document.createElement('p');
    elementP.innerHTML = "<b>include </b><input type=\"text\">;";
    parentElement.insertBefore(elementP, afterElement.nextSibling);
}

//Sorry for hardcode
function prepareData() {
    var result = {};

    //Block main
    var main = {};
    main['user'] = document.getElementById('input_user').value;
    main['worker_process'] = document.getElementById('input_worker_process').value;
    main['worker_rlimit_nofile'] = document.getElementById('input_worker_rlimit_nofile').value;
    main['pid'] = document.getElementById('input_pid').value;
    main['error_log'] = document.getElementById('input_error_log').value;
    result['main'] = main;

    //Block events
    var events = {};
    events['connections'] = document.getElementById('input_connections').value;
    events['worker_connections'] = document.getElementById('input_worker_connections').value;
    events['worker_connections'] = document.getElementById('input_worker_connections').value;
    var useList = document.getElementsByName('input_use_item');
    for (var i = 0; i < useList.length; i++) {
        if (useList.item(i).checked) {
            events['use'] = useList.item(i).value;
        }
    }
    result['events'] = events;

    //Block http
    var http = {};
//    var include_http = [];
//    for (var i = 0; i < useList.length; i++) {
//        include_http.append(useList.item(i).value);
//    }
//    http['include'] = include_http;
//    http['default_type'] = document.getElementById('input_default_type').value;
//    http['log_format'] = document.getElementById('textarea_log_format').value;
//    if (document.getElementById('input_sendfile').checked) {
//        http['sendfile'] = "on";
//    } else {
//        http['sendfile'] = "off";
//    }
//    if (document.getElementById('input_tcp_nopush').checked) {
//        http['tcp_nopush'] = "on";
//    } else {
//        http['tcp_nopush'] = "off";
//    }
//    if (document.getElementById('input_tcp_nodelay').checked) {
//        http['tcp_nodelay'] = "on";
//    } else {
//        http['tcp_nodelay'] = "off";
//    }
//    if (document.getElementById('input_server_tokens').checked) {
//        http['server_tokens'] = "on";
//    } else {
//        http['server_tokens'] = "off";
//    }
//    if (document.getElementById('input_gzip').checked) {
//        http['gzip'] = "on";
//    } else {
//        http['gzip'] = "off";
//    }
//    if (document.getElementById('input_gzip_static').checked) {
//        http['gzip_static'] = "on";
//    } else {
//        http['gzip_static'] = "off";
//    }
//    if (document.getElementById('input_gzip_vary').checked) {
//        http['gzip_vary'] = "on";
//    } else {
//        http['gzip_vary'] = "off";
//    }
//    http['gzip_comp_level'] = document.getElementById('input_gzip_comp_level').value;
//    http['gzip_min_length'] = document.getElementById('input_gzip_min_length').value;
//    http['gzip_proxied'] = document.getElementById('input_gzip_proxied').value;
//    http['gzip_types'] = document.getElementById('input_gzip_types').value;
//    http['gzip_http_version'] = document.getElementById('input_gzip_http_version').value;
//    http['gzip_disable'] = document.getElementById('input_gzip_disable').value;
//    http['keepalive_timeout'] = document.getElementById('input_keepalive_timeout').value;
//    http['limit_conn_zone'] = document.getElementById('input_limit_conn_zone').value;
//
//    //BlockServer


    result['http'] = http;

    $.ajax({
        type: "POST",
        url: "/nginx/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            result: result
        },
//        success: function(data) {
//            alert("Congratulations! You scored: "+data);
//        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}
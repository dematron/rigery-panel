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

function prepareData() {
    var result = {"a":"a", "b":"b"};
    result.h = "h";
    var object = document.getElementById('details_location');
    key = object.id;
    result[key] = object.id;
    for (var childItem in object.childNodes) {
        var key = childItem.id;
        result[key] = childItem.id;
    }


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
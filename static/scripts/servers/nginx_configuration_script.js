/**
 * Created by kutepoval on 20.05.14.
 */

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

function deleteLocation(element) {
    var elements = element.parentNode.getElementsByTagName("details");
    if (elements.length>1) {
        element.previousElementSibling.remove();
        element.remove();
    }
}

function createServer(parentElement) {
    var serverBlock = document.getElementById('details_server');
    var newServerBlock = serverBlock.cloneNode(true);
    parentElement.appendChild(newServerBlock);
}

function deleteServer(element) {
    var elements = document.getElementsByName("details_server");
    if (elements.length>1) {
        element.remove();
    }
}


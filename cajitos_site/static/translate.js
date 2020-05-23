function translate(sourceElemId, destElemId, destLang) {

    var request = new XMLHttpRequest();
    request.open('POST', '/service/translate', true);

    var sourceElem = document.getElementById(sourceElemId);
    var destElem = document.getElementById(destElemId);

    destElem.innerHTML = '<img src=' + image + '>';

    var json = JSON.stringify({
        text: sourceElem.innerText,
        dest_language: destLang
    });

    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            destElem.innerText = this.response
        } else {
            destElem.innerText = _('Error occurred while performing translation ');
        }
    };

    request.onerror = function () {
        destElem.innerText = _('Connection error');
    };

    request.send(json);
}
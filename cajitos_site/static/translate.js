function translate_v2(sourceElemId, destElemId, destLang) {

    var request = new XMLHttpRequest();
    request.open('POST', '/service/translate', true);

    var sourceElem = document.getElementById(sourceElemId);
    var destElem = document.getElementById(destElemId);

    var json = JSON.stringify({
        text: sourceElem.innerText,
        dest_language: destLang
    });

    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            destElem.innerText = this.response
        } else {
            console.log('Fuck off');
        }
    };

    request.onerror = function () {
        console.log('Fuck off also');
    };

    request.send(json);
}
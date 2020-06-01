function translate(sourceElemId, destElemId, destLang) {

    var request = new XMLHttpRequest();
    request.open('POST', '/translate', true);

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

function flip_card_value() {
    let faceEl = document.getElementById('translation');
    let backEl = document.getElementById('backtranslation');


    let facetext = faceEl.innerText;
    faceEl.innerText = backEl.value;
    backEl.value = facetext;
}


function request_new_card() {

    var request = new XMLHttpRequest();
    request.open('GET', '/things/random_card?raw=1', true);

    elemTitle = document.getElementById('card_title');
    elemAuthor = document.getElementById('author_username');
    elemOrigin = document.getElementById('translation');
    elemTranslation = document.getElementById('backtranslation');

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            data = JSON.parse(this.response);
            elemTitle.innerText = data.part_of_speech;
            elemAuthor.innerText = data.author.username;
            elemOrigin.innerText = data.origin;
            elemTranslation.value = data.translation;
        } else {
            elemOrigin.innerText = _('Error occurred');
        }
    };

    request.onerror = function () {
        elemOrigin.innerText = _('Connection error');
    };

    request.send();
}
function flip_card(face, back) {
    translation_field = document.getElementById('translation');
    if (translation_field.innerText === face) {
        translation_field.innerText=back;
    }
    else {
        translation_field.innerText=face;
    }
}
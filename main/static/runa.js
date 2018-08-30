function runa() {
    var runaNumber=Math.floor((Math.random() * 25) + 1); /* random number between 1 and 25*/
    runa_image = document.getElementById('runaimg');
    // runa_image.src="{{ url_for('static', filename='images/runa{{ runaNumber }}.jpg') }}";
    // runa_image.src="images/runa"+ runaNumber +".jpg";  /*change image for corresponding runa*/
    sense = runas_sense[runaNumber];
    var prediction = sense[0];
    if (sense.length > 1) {
        var is_inverse=Math.round(Math.random());
        prediction = sense[is_inverse];
        runa_image.style.transform = "rotate(180deg)";
    }
    document.getElementById("text_runa").value=prediction;
}
function Begin(){
// document.getElementById("runaimg").src="images/runa25.jpg";
document.getElementById("text_runa").value="Тут будет Ваше предсказание";
}

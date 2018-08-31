function runa() {
    var runaNumber=Math.floor((Math.random() * 25) + 1); /* random number between 1 and 25*/
    runa_image = document.getElementById('runaimg');
    runa_image.style.removeProperty('transform');
    runa_image.src=runs[runaNumber-1];  /*change image for corresponding runa*/
    sense = runas_sense[runaNumber];
    var prediction = sense[0];
    if (sense.length > 1) {
        var is_inverse=Math.round(Math.random());
        if (is_inverse) {
          runa_image.style.transform = "rotate(180deg)";
          prediction = sense[is_inverse];
        }
    }
    document.getElementById("text_runa").value=prediction;
}
function begin(){
document.getElementById("runaimg").src="images/runa25.jpg";
document.getElementById("text_runa").value="Тут будет Ваше предсказание";
}

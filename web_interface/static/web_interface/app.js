function move(id, time) {
    console.log(time);
    intv = ((time*1000) / 100) * 0.95;
    console.log(intv)
    var elem = document.getElementById(id);
    var elem2 = document.getElementById('loader').style.visibility='visible';
    var width = 1;
    var id = setInterval(frame, intv);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++;
            elem.style.width = width + '%';
        }
    }
}

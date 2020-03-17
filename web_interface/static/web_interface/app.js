// this moves the pouring status bar
function move(id, time) {
    console.log(time);
    intv = ((time*1000) / 100) * 0.95;
    console.log(intv)
    var elem = document.getElementById(id);
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

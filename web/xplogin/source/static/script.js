window.addEventListener('load', eventWindowLoaded, false);

function eventWindowLoaded() {
    canvasApp();

}

function canvasApp() {


    var theCanvas = document.getElementById("canvas");
    var context = theCanvas.getContext("2d");

    drawScreen();

    function drawScreen() {
        context.beginPath(); // top left; red
        context.strokeStyle = "#F75A14";
        context.lineWidth = 1;
        context.moveTo(12, 10);
        context.quadraticCurveTo(30, 5, 37, 13);
        context.lineTo(32, 26);
        context.quadraticCurveTo(30, 22, 6, 22.5);
        context.lineTo(12, 10);
        context.closePath();
        context.lineWidth = 1;
        context.fillStyle = '#F75A14';
        context.fill();
        context.strokeStyle = '#F75A14';
        context.stroke();

        context.beginPath(); // top right; green
        context.strokeStyle = "#96C93D";
        context.lineWidth = 1;
        context.moveTo(40, 14);
        context.quadraticCurveTo(49, 18, 63, 17);
        context.lineTo(57, 32);
        context.quadraticCurveTo(49, 35, 34, 28);
        context.lineTo(40, 14);
        context.closePath();
        context.fillStyle = '#96C93D';
        context.fill();
        context.strokeStyle = '#96C93D';
        context.stroke();


        context.beginPath(); // bottom right; yellow
        context.strokeStyle = "#FACC13";
        context.lineWidth = 1;
        context.moveTo(33, 30);
        context.quadraticCurveTo(47, 37, 56, 35);
        context.lineTo(49, 50);
        context.quadraticCurveTo(40, 52, 27, 45);
        context.lineTo(33, 30);
        context.closePath();
        context.fillStyle = "#FACC13";
        context.fill();
        context.strokeStyle = "#FACC13";
        context.stroke();


        context.beginPath(); // bottom left; blue
        context.strokeStyle = "#8BA4FD";
        context.lineWidth = 1;
        context.moveTo(30, 29);
        context.quadraticCurveTo(30, 24, 5, 25);
        context.lineTo(0, 40);
        context.quadraticCurveTo(20, 40, 24, 43);
        context.lineTo(30, 29);
        context.closePath();
        context.fillStyle = "#8BA4FD";
        context.fill();
        context.strokeStyle = "#8BA4FD";
        context.stroke();

    }
}
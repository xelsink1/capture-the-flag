function drawGrass(){    
    var ctx = canvas.getContext('2d')      
    var testImage = new Image();
    testImage.src = "CAPTURE-THE-FLAG/static/res/grass.jpg";
    testImage.onload = function (){
        ctx.drawImage(testImage, 10, 50)
    }
}


function return_json(){
    fetch('http://192.168.239.71:3333/api/state',
        ).then(response => {
            console.log(response)
            return response.json()
        }
        ).then(data => {
            console.log(data);
                alert(data.height)
        });
}
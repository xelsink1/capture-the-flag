var ctx = canvas.getContext('2d')
data = undefined
var images = {}
images.stone = new Image();
images.stone.src = "/static/res/stone.jpg";

images.grass = new Image();
images.grass.src = "/static/res/grass_new.jpg";

images.base = new Image();
images.base.src = "/static/res/base.jpg";


images.player_UP = new Image();
images.player_UP.src = "/static/res/player_UP.jpg";

images.player_DOWN = new Image();
images.player_DOWN.src = "/static/res/player_DOWN.jpg";

images.player_RIGHT = new Image();
images.player_RIGHT.src = "/static/res/player_RIGHT.jpg";

images.player_LEFT = new Image();
images.player_LEFT.src = "/static/res/player_LEFT.jpg";




function drawGrass(){    
    for (var i = 0; i < 32; i++){
        for (var j = 0; j < 32; j++){
            ctx.drawImage(images.grass, 30 * i, 30 * j, 30, 30)
        }
    }
}

function game_loop_iteration()  
{
    if (!data) return
    drawGrass()
    data['objects'].forEach((object) => {
        if (object['type'] == 'wall') {
            drawStone(object['x'], object['y'])
        }
    })
    data['bases'].forEach((base) => {
        drawBase(base['x'], base['y'])  
    })
    data['players'].forEach((player) => {
        drawPlayer(player['x'], player['y'])
    })
}


// функции по отрисовке
function drawStone(x, y){
    return ctx.drawImage(images.stone, x * 30, y * 30, 30, 30)
}

function drawBase(x, y){
    return ctx.drawImage(images.base, x * 30, y * 30, 30, 30)
}

function drawPlayer(x, y, side){
    // if (side == "up")
    //     return ctx.drawImage(images.player_UP, x * 30, y * 30, 30, 30)
    // if (side == "down")
    //     return ctx.drawImage(images.player_DOWN, x * 30, y * 30, 30, 30)
    // if (side == "left")
    //     return ctx.drawImage(images.player_LEFT, x * 30, y * 30, 30, 30)
    // if (side == "right")
    //     return ctx.drawImage(images.player_RIGHT, x * 30, y * 30, 30, 30)
    // }
    return ctx.drawImage(images.player_RIGHT, x * 30, y * 30, 30, 30)
}
// function drawBullet()
// function drawPlayer(){
// var ctx = canvas.getContext('2d')
// var image = new Image();
// image.src = "/static/res/red_square.jpg";  
// image.onload = function (){
//     ctx.drawImage(image, 510, 300, 30, 30)
//     }
// }


function update_map(){
    fetch('/api/state',
        ).then(response => {
            return response.json()
        }
        ).then(answer => {
            data = answer
            game_loop_iteration()
            console.log(data)
        });
}

setInterval(update_map, 1000)

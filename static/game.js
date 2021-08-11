var ctx = canvas.getContext('2d')
data = undefined
var images = {}
images.stone = new Image();
images.stone.src = "/static/res/stone.jpg";

images.grass = new Image();
images.grass.src = "/static/res/grass_new.jpg";

images.base = new Image();
images.base.src = "/static/res/base.png";

images.watermelon = new Image();
images.watermelon.src = "/static/res/watermelon.png"

images.player_UP = new Image();
images.player_UP.src = "/static/res/player_UP.jpg";
images.player_DOWN = new Image();
images.player_DOWN.src = "/static/res/player_DOWN.jpg";
images.player_RIGHT = new Image();
images.player_RIGHT.src = "/static/res/player_RIGHT.jpg";
images.player_LEFT = new Image();
images.player_LEFT.src = "/static/res/player_LEFT.jpg";

//images.player_UP = new Image();
//images.bullet_UP.src = "/static/res/bullet_UP.png";
//images.bullet_DOWN = new Image();
//images.bullet_DOWN.src = "/static/res/bullet_DOWN.png";
//images.bullet_RIGHT = new Image();
//images.bullet_RIGHT.src = "/static/res/bullet_RIGHT.png";
//images.bullet_LEFT = new Image();
//images.bullet_LEFT.src = "/static/res/bullet_LEFT.png";



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
        // if (object['type'] == 'flag') {
        //     drawWatermelon(object['x'], object['y'])
        // } 
    })
    data['bases'].forEach((base) => {
        drawBase(base['x'], base['y'])  
    })
    data['players'].forEach((player) => {
        drawPlayer(player['x'], player['y'], player['side'])
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
     if (side == "up"){
        return ctx.drawImage(images.player_UP, x * 30, y * 30, 30, 30)
    }
     if (side == "down"){
        return ctx.drawImage(images.player_DOWN, x * 30, y * 30, 30, 30)
    }
     if (side == "left"){
        return ctx.drawImage(images.player_LEFT, x * 30, y * 30, 30, 30)
    }
     if (side == "right"){
        return ctx.drawImage(images.player_RIGHT, x * 30, y * 30, 30, 30)
    }
}

function drawBullet(x, y, side){
        if (side == "up"){
            return ctx.drawImage(images.bullet_UP, x * 30, y * 30, 30, 30)
        }
        if (side == "down"){
            return ctx.drawImage(images.bullet_DOWN, x * 30, y * 30, 30, 30)
        }
        if (side == "left"){
            return ctx.drawImage(images.bullet_LEFT, x * 30, y * 30, 30, 30)
        }
        if (side == "right"){
            return ctx.drawImage(images.bullet_RIGHT, x * 30, y * 30, 30, 30)
        }
}

function drawWatermelon(x, y){
    return ctx.drawImage(images)
}



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

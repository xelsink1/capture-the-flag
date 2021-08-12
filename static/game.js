var ctx = canvas.getContext('2d')
data = undefined
var images = {}
images.stone_3hp = new Image();
images.stone_3hp.src = "/static/res/stone_3hp.jpg";
images.stone_2hp = new Image();
images.stone_2hp.src = "/static/res/stone_2hp.png";
images.stone_1hp = new Image();
images.stone_1hp.src = "/static/res/stone_1hp.png";


images.grass = new Image();
images.grass.src = "/static/res/grass_new.jpg";


images.flag = new Image();
images.flag.src = "/static/res/flag.png"

images.medkit = new Image();
images.medkit.src = "/static/res/medkit.png"

images.ammo = new Image();
images.ammo.src = "/static/res/ammo.png"


images.base_UKR = new Image();
images.base_UKR.src = "/static/res/UKR.png";
images.base_GERM = new Image();
images.base_GERM.src = "/static/res/GERM.png";
images.base_USA = new Image();
images.base_USA.src = "/static/res/USA.png";
images.base_RUS = new Image();
images.base_RUS.src = "/static/res/RUS.png";

images.player_UP_hasF = new Image();
images.player_UP_hasF.src = "/static/res/player_UP_hasF.png";
images.player_DOWN_hasF = new Image();
images.player_DOWN_hasF.src = "/static/res/player_DOWN_hasF.png";
images.player_RIGHT_hasF = new Image();
images.player_RIGHT_hasF.src = "/static/res/player_RIGHT_hasF.png";
images.player_LEFT_hasF = new Image();
images.player_LEFT_hasF.src = "/static/res/player_LEFT_hasF.png";
images.player_UP = new Image();
images.player_UP.src = "/static/res/player_UP.jpg";
images.player_DOWN = new Image();
images.player_DOWN.src = "/static/res/player_DOWN.jpg";
images.player_RIGHT = new Image();
images.player_RIGHT.src = "/static/res/player_RIGHT.jpg";
images.player_LEFT = new Image();
images.player_LEFT.src = "/static/res/player_LEFT.jpg";



images.bullet_UP = new Image();
images.bullet_UP.src = "/static/res/bullet_UP.png"
images.bullet_DOWN = new Image();
images.bullet_DOWN.src = "/static/res/bullet_DOWN.png";
images.bullet_RIGHT = new Image();
images.bullet_RIGHT.src = "/static/res/bullet_RIGHT.png";
images.bullet_LEFT = new Image();
images.bullet_LEFT.src = "/static/res/bullet_LEFT.png";


function drawGrass() {
    for (var i = 0; i < 32; i++) {
        for (var j = 0; j < 32; j++) {
            ctx.drawImage(images.grass, 30 * i, 30 * j, 30, 30)
        }
    }
}
// обновление кадров игры
function game_loop_iteration() {
    if (!data) return
    drawGrass()

    data['objects'].forEach((object) => {
        if (object['type'] == 'wall') {
            drawStone(object['x'], object['y'], object['hp'])
        }
        if (object['type'] == 'flag') {
            drawFlag(object['x'], object['y'])
        }
        if (object['type'] == 'medkit') {
            drawMedkit(object['x'], object['y'])
        }
        if (object['type'] == 'ammo') {
            drawAmmo(object['x'], object['y'])
        }
    })
    data['bases'].forEach((base) => {
        drawBase(base['x'], base['y'], base['id'])
    })
    data['bullets'].forEach((bullet) => {
        drawBullet(bullet['x'], bullet['y'], bullet['side'])
    })
    data['players'].forEach((player) => {
        drawPlayer(player['x'], player['y'], player['side'], player['has_flag'])
    })
}

// функции по отрисовке
function drawStone(x, y, hp) {
    if (hp == 3) {
        return ctx.drawImage(images.stone_3hp, x * 30, y * 30, 30, 30)
    }
    if (hp == 2) {
        return ctx.drawImage(images.stone_2hp, x * 30, y * 30, 30, 30)
    }
    if (hp == 1) {
        return ctx.drawImage(images.stone_1hp, x * 30, y * 30, 30, 30)
    }
}

function drawFlag(x, y) {
    return ctx.drawImage(images.flag, x * 30, y * 30, 30, 30)
}
function drawMedkit(x, y) {
    return ctx.drawImage(images.medkit, x * 30, y * 30, 30, 30)
}
function drawBase(x, y, id) {
    if (id == 1) {
        return ctx.drawImage(images.base_UKR, x * 30, y * 30, 30, 30)
    }
    if (id == 2) {
        return ctx.drawImage(images.base_USA, x * 30, y * 30, 30, 30)
    }
    if (id == 3) {
        return ctx.drawImage(images.base_RUS, x * 30, y * 30, 30, 30)
    }
    if (id == 4) {
        return ctx.drawImage(images.base_GERM, x * 30, y * 30, 30, 30)
    }
}
function drawAmmo(x, y) {
    return ctx.drawImage(images.ammo, x * 30, y * 30, 30, 30)
}

function drawPlayer(x, y, side, has_flag) {
    ctx.drawImage(images.player_UP, x * 30, y * 30, 30, 30)
    if (has_flag == true) {
        if (side == "up") {
            return ctx.drawImage(images.player_UP_hasF, x * 30, y * 30, 30, 30)
        }
        if (side == "down") {
            return ctx.drawImage(images.player_DOWN_hasF, x * 30, y * 30, 30, 30)
        }
        if (side == "left") {
            return ctx.drawImage(images.player_LEFT_hasF, x * 30, y * 30, 30, 30)
        }
        if (side == "right") {
            return ctx.drawImage(images.player_RIGHT_hasF, x * 30, y * 30, 30, 30)
        }
    }
    if (has_flag == false) {
        if (side == "up") {
            return ctx.drawImage(images.player_UP, x * 30, y * 30, 30, 30)
        }
        if (side == "down") {
            return ctx.drawImage(images.player_DOWN, x * 30, y * 30, 30, 30)
        }
        if (side == "left") {
            return ctx.drawImage(images.player_LEFT, x * 30, y * 30, 30, 30)
        }
        if (side == "right") {
            return ctx.drawImage(images.player_RIGHT, x * 30, y * 30, 30, 30)
        }
    }

}

function drawBullet(x, y, side) {
    if (side == "up") {
        return ctx.drawImage(images.bullet_UP, x * 30, y * 30, 30, 30)
    }
    if (side == "down") {
        return ctx.drawImage(images.bullet_DOWN, x * 30, y * 30, 30, 30)
    }
    if (side == "left") {
        return ctx.drawImage(images.bullet_LEFT, x * 30, y * 30, 30, 30)
    }
    if (side == "right") {
        return ctx.drawImage(images.bullet_RIGHT, x * 30, y * 30, 30, 30)
    }
}

function update_map() {
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

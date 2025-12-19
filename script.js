const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

const buttons = document.querySelectorAll(".nav-btn");
const pages = document.querySelectorAll(".page");
const profilePic = document.getElementById("profilePic");
const changePhotoBtn = document.getElementById("changePhotoBtn");
const photoInput = document.getElementById("photoInput");
const toggleThemeBtn = document.getElementById("toggleTheme");
const body = document.body;

// Переключение страниц
buttons.forEach(btn => {
    btn.onclick = () => {
        const pageId = btn.dataset.page;
        pages.forEach(p => p.classList.remove("active"));
        document.getElementById(pageId).classList.add("active");

        buttons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
    }
});

// Показать первую страницу
pages[0].classList.add("active");
buttons[0].classList.add("active");

// Только ты можешь менять фото
const MY_ID = 6342709681; // <- Вставь свой Telegram ID
if(tg.initDataUnsafe.user.id === MY_ID){
    changePhotoBtn.style.display = 'inline-block';
} else {
    changePhotoBtn.style.display = 'none';
}

// Изменение фото
changePhotoBtn.onclick = () => {
    photoInput.click();
};

photoInput.onchange = () => {
    const file = photoInput.files[0];
    if(file){
        const reader = new FileReader();
        reader.onload = (e) => {
            profilePic.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

// Темный / светлый режим
toggleThemeBtn.onclick = () => {
    body.classList.toggle("light");
};

// ------------------ Снег ------------------
const canvas = document.getElementById('snowCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let snowflakes = [];

function createSnowflakes() {
    for(let i=0; i<100; i++){
        snowflakes.push({
            x: Math.random()*canvas.width,
            y: Math.random()*canvas.height,
            radius: Math.random()*3 + 1,
            speed: Math.random()*1 + 0.5
        });
    }
}

function drawSnowflakes() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = 'white';
    ctx.beginPath();
    snowflakes.forEach(f => {
        ctx.moveTo(f.x, f.y);
        ctx.arc(f.x, f.y, f.radius, 0, Math.PI*2);
    });
    ctx.fill();
    moveSnowflakes();
}

function moveSnowflakes() {
    snowflakes.forEach(f => {
        f.y += f.speed;
        if(f.y > canvas.height){
            f.y = 0;
            f.x = Math.random()*canvas.width;
        }
    });
}

function animateSnow() {
    drawSnowflakes();
    requestAnimationFrame(animateSnow);
}

window.addEventListener('resize', ()=>{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

createSnowflakes();
animateSnow();

// ------------------ Мини игра динозавра ------------------
const dinoCanvas = document.getElementById('dinoGame');
const dinoCtx = dinoCanvas.getContext('2d');
let dino = { x: 50, y: 120, width: 20, height: 20, vy: 0, gravity: 0.6, jump: -12 };
let obstacles = [];
let frame = 0;
let gameOver = false;

function spawnObstacle() {
    obstacles.push({ x: 400, y: 130, width: 20, height: 20 });
}

function updateGame() {
    dino.vy += dino.gravity;
    dino.y += dino.vy;
    if(dino.y > 130) { dino.y = 130; dino.vy = 0; }
    dinoCtx.clearRect(0,0,400,150);

    // Динозавр
    dinoCtx.fillStyle = '#555';
    dinoCtx.fillRect(dino.x, dino.y, dino.width, dino.height);

    // Объекты
    dinoCtx.fillStyle = '#f00';
    obstacles.forEach(ob => {
        ob.x -= 4;
        dinoCtx.fillRect(ob.x, ob.y, ob.width, ob.height);
    });

    // Проверка коллизий
    obstacles.forEach(ob => {
        if(dino.x < ob.x + ob.width && dino.x + dino.width > ob.x &&
           dino.y < ob.y + ob.height && dino.y + dino.height > ob.y){
               gameOver = true;
        }
    });

    obstacles = obstacles.filter(ob => ob.x + ob.width > 0);

    if(frame % 120 === 0) spawnObstacle();

    frame++;
    if(!gameOver) requestAnimationFrame(updateGame);
    else dinoCtx.fillText("GAME OVER", 150,75);
}

document.addEventListener('keydown', (e)=>{
    if(e.code === "Space" && dino.y >= 130) dino.vy = dino.jump;
});

updateGame();
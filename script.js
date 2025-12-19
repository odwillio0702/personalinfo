const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

const profilePic = document.getElementById("profilePic");
const changePhotoBtn = document.getElementById("changePhotoBtn");
const photoInput = document.getElementById("photoInput");

// Только ты можешь менять фото
const MY_ID = 6342709681; // <- вставь свой Telegram ID
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
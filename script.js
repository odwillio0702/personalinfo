// ==================== FADE-IN ====================
const faders = document.querySelectorAll('.fade-in');

const appearOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
};

const appearOnScroll = new IntersectionObserver(function(entries, observer){
    entries.forEach(entry => {
        if(entry.isIntersecting){
            entry.target.classList.add('fade-in-visible');
            observer.unobserve(entry.target);
        }
    });
}, appearOptions);

faders.forEach(fader => {
    appearOnScroll.observe(fader);
});

// ==================== ПАРТИКЛЫ / ТУМАН ====================
const canvas = document.createElement('canvas');
canvas.className = 'particles';
document.body.appendChild(canvas);
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particlesArray = [];
const particlesCount = 100;

for(let i = 0; i < particlesCount; i++){
    particlesArray.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 2 + 1,
        speedX: Math.random() * 0.5 - 0.25,
        speedY: Math.random() * 0.5 - 0.25,
        alpha: Math.random() * 0.5 + 0.2
    });
}

function animateParticles(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    particlesArray.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2);
        ctx.fillStyle = `rgba(255,255,255,${p.alpha})`;
        ctx.fill();
        p.x += p.speedX;
        p.y += p.speedY;
        if(p.x < 0) p.x = canvas.width;
        if(p.x > canvas.width) p.x = 0;
        if(p.y < 0) p.y = canvas.height;
        if(p.y > canvas.height) p.y = 0;
    });
    requestAnimationFrame(animateParticles);
}

animateParticles();

window.addEventListener('resize', ()=>{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// ==================== TELEGRAM WEBAPP ====================
const tg = window.Telegram?.WebApp;
const ADMIN_ID = 6342709681; // твой айди, если нужно для админки

function sendUserData() {
    if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
        const user = tg.initDataUnsafe.user;
        tg.sendData(JSON.stringify({
            action: "log_user",
            id: user.id,
            first_name: user.first_name,
            last_name: user.last_name || "",
            username: user.username || ""
        }));
        console.log("User data sent:", user);
    }
}

// Автоотправка при открытии WebApp
sendUserData();

// ==================== КНОПКА ДЛЯ РУЧНОЙ ОТПРАВКИ ====================
const sendUserDataButton = document.createElement('button');
sendUserDataButton.textContent = "Отправить данные боту";
sendUserDataButton.style.position = "fixed";
sendUserDataButton.style.bottom = "20px";
sendUserDataButton.style.left = "50%";
sendUserDataButton.style.transform = "translateX(-50%)";
sendUserDataButton.style.padding = "10px 20px";
sendUserDataButton.style.background = "#6a0dad";
sendUserDataButton.style.color = "#fff";
sendUserDataButton.style.border = "none";
sendUserDataButton.style.borderRadius = "10px";
sendUserDataButton.style.cursor = "pointer";
sendUserDataButton.style.zIndex = "1000";
document.body.appendChild(sendUserDataButton);

sendUserDataButton.addEventListener('click', sendUserData);
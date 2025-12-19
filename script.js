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

changePhotoBtn.onclick = () => photoInput.click();

photoInput.onchange = () => {
    const file = photoInput.files[0];
    if(file){
        const reader = new FileReader();
        reader.onload = (e) => { profilePic.src = e.target.result; };
        reader.readAsDataURL(file);
    }
};

// ------------------ Fade-in ------------------
const faders = document.querySelectorAll('.fade-in');
const appearOptions = { threshold: 0.2, rootMargin: "0px 0px -50px 0px" };
const appearOnScroll = new IntersectionObserver(function(entries, observer){
    entries.forEach(entry => {
        if(entry.isIntersecting){
            entry.target.classList.add('fade-in-visible');
            observer.unobserve(entry.target);
        }
    });
}, appearOptions);
faders.forEach(fader => appearOnScroll.observe(fader));

// ------------------ Typing text ------------------
const typingTexts = document.querySelectorAll('.typing-text');
typingTexts.forEach(el => {
    const text = el.dataset.text;
    let index = 0;
    function type(){
        if(index <= text.length){
            el.textContent = text.slice(0,index);
            index++;
            setTimeout(type, 100);
        }
    }
    type();
});

// ------------------ Slider ------------------
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
document.getElementById('nextSlide').onclick = () => {
    slides[currentSlide].classList.remove('active');
    currentSlide = (currentSlide+1)%slides.length;
    slides[currentSlide].classList.add('active');
};
document.getElementById('prevSlide').onclick = () => {
    slides[currentSlide].classList.remove('active');
    currentSlide = (currentSlide-1+slides.length)%slides.length;
    slides[currentSlide].classList.add('active');
};

// ------------------ Fog ------------------
const canvas = document.getElementById('fogCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let fogParticles = [];
function createFog(){
    for(let i=0;i<200;i++){
        fogParticles.push({
            x: Math.random()*canvas.width,
            y: Math.random()*canvas.height,
            radius: Math.random()*3 + 1,
            speed: Math.random()*0.3 + 0.1
        });
    }
}
function drawFog(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = 'rgba(255,255,255,0.05)';
    fogParticles.forEach(f=>{
        ctx.beginPath();
        ctx.arc(f.x,f.y,f.radius,0,Math.PI*2);
        ctx.fill();
        f.y -= f.speed;
        if(f.y <0){ f.y=canvas.height; f.x=Math.random()*canvas.width; }
    });
}
function animateFog(){
    drawFog();
    requestAnimationFrame(animateFog);
}
window.addEventListener('resize', ()=>{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
createFog();
animateFog();

// ------------------ Random green exclamation marks ------------------
function spawnExclamations(){
    const mark = document.createElement('div');
    mark.textContent = '!';
    mark.style.position = 'fixed';
    mark.style.color = 'lime';
    mark.style.fontSize = (Math.random()*30+20)+'px';
    mark.style.left = Math.random()*window.innerWidth+'px';
    mark.style.top = Math.random()*window.innerHeight+'px';
    mark.style.zIndex = 2;
    mark.style.pointerEvents = 'none';
    document.body.appendChild(mark);
    setTimeout(()=>mark.remove(),3000);
}
setInterval(spawnExclamations, 1000);
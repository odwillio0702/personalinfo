// ------------------ Swipe Slider ------------------
const sliderInner = document.querySelector('.slider-inner');
const slides = document.querySelectorAll('.slide');
let currentSlide = 0;

function updateSlider() {
    const offset = -currentSlide * 100;
    sliderInner.style.transform = `translateX(${offset}%)`;
}

// Touch swipe
let startX = 0;
let endX = 0;

sliderInner.addEventListener('touchstart', (e)=>{
    startX = e.touches[0].clientX;
});

sliderInner.addEventListener('touchmove', (e)=>{
    endX = e.touches[0].clientX;
});

sliderInner.addEventListener('touchend', ()=>{
    const diff = startX - endX;
    if(Math.abs(diff) > 50){
        if(diff > 0){
            currentSlide = (currentSlide + 1) % slides.length;
        } else {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        }
        updateSlider();
    }
    startX = 0;
    endX = 0;
});

// Инициализация
updateSlider();
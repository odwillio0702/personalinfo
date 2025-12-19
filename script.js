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

// Показываем первый слайд сразу
slides[0].classList.add('active');
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

const buttons = document.querySelectorAll(".nav-btn");
const pages = document.querySelectorAll(".page");
const profilePic = document.getElementById("profilePic");
const changePhotoBtn = document.getElementById("changePhotoBtn");
const photoInput = document.getElementById("photoInput");

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

// Показать первую страницу по умолчанию
pages[0].classList.add("active");
buttons[0].classList.add("active");

// Проверка User ID (только для тебя)
const MY_ID = 6342709681; // Твой Telegram ID
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
            // Тут можно добавить отправку фото боту для сохранения
        };
        reader.readAsDataURL(file);
    }
};
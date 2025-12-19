const tg = window.Telegram.WebApp;
tg.ready();

const CHAT_ID = tg.initDataUnsafe.user.id;

// 🔴 ВАЖНО: сюда вставь URL сервера (Railway / Render)
const SERVER_URL = "https://telegram-schedulebot.vercel.app/";

const form = document.getElementById("reminderForm");
const output = document.getElementById("output");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const text = document.getElementById("text").value;
    const time = document.getElementById("time").value;
    const days = document.getElementById("days").value;

    try {
        const res = await fetch(SERVER_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                chat_id: CHAT_ID,
                text,
                time,
                days
            })
        });

        if (res.ok) {
            output.innerText = "✅ Напоминание создано!";
            tg.HapticFeedback.notificationOccurred("success");
            form.reset();
        } else {
            output.innerText = "❌ Ошибка при создании";
        }
    } catch (err) {
        output.innerText = "❌ Сервер недоступен";
    }
});
const daysInput = document.getElementById("days");
const weekdaysBtn = document.getElementById("weekdaysBtn");

weekdaysBtn.addEventListener("click", () => {
    daysInput.value = "mon,tue,wed,thu,fri";
    tg.HapticFeedback.impactOccurred("light");
});
const tg = window.Telegram.WebApp;
tg.ready();

const SERVER_URL = "https://telegram-schedulebot.vercel.app/";

const form = document.getElementById("reminderForm");
const output = document.getElementById("output");
const daysInput = document.getElementById("days");

const selectedDays = new Set();

document.querySelectorAll(".day").forEach(btn => {
    btn.addEventListener("click", () => {
        const day = btn.dataset.day;

        if (selectedDays.has(day)) {
            selectedDays.delete(day);
            btn.classList.remove("active");
        } else {
            selectedDays.add(day);
            btn.classList.add("active");
        }

        daysInput.value = [...selectedDays].join(",");
        tg.HapticFeedback.impactOccurred("light");
    });
});

function setDays(days) {
    selectedDays.clear();
    document.querySelectorAll(".day").forEach(btn => {
        const on = days.includes(btn.dataset.day);
        btn.classList.toggle("active", on);
        if (on) selectedDays.add(btn.dataset.day);
    });
    daysInput.value = days.join(",");
}

document.getElementById("weekdays").onclick = () =>
    setDays(["mon","tue","wed","thu","fri"]);

document.getElementById("alldays").onclick = () =>
    setDays(["mon","tue","wed","thu","fri","sat","sun"]);

form.addEventListener("submit", async e => {
    e.preventDefault();

    if (!daysInput.value) {
        output.innerText = "❌ Выбери дни";
        return;
    }

    const payload = {
        chat_id: tg.initDataUnsafe.user.id,
        text: text.value,
        time: time.value,
        days: daysInput.value
    };

    const res = await fetch(SERVER_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        output.innerText = "✅ Напоминание создано";
        form.reset();
        selectedDays.clear();
        document.querySelectorAll(".day").forEach(b => b.classList.remove("active"));
        daysInput.value = "";
    } else {
        output.innerText = "❌ Ошибка";
    }
});
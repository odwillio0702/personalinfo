const tg = window.Telegram.WebApp;
tg.ready();

const SERVER_URL = "https://telegram-schedulebot.vercel.app/";

const form = document.getElementById("reminderForm");
const output = document.getElementById("output");
const daysInput = document.getElementById("days");

const selected = new Set();

document.querySelectorAll(".days-grid button").forEach(btn => {
    btn.addEventListener("click", () => {
        const day = btn.dataset.day;

        if (selected.has(day)) {
            selected.delete(day);
            btn.classList.remove("active");
        } else {
            selected.add(day);
            btn.classList.add("active");
        }

        daysInput.value = [...selected].join(",");
        tg.HapticFeedback.impactOccurred("light");
    });
});

function applyDays(days) {
    selected.clear();
    document.querySelectorAll(".days-grid button").forEach(b => {
        b.classList.toggle("active", days.includes(b.dataset.day));
        if (days.includes(b.dataset.day)) selected.add(b.dataset.day);
    });
    daysInput.value = days.join(",");
}

document.getElementById("weekdays").onclick = () =>
    applyDays(["mon","tue","wed","thu","fri"]);

document.getElementById("alldays").onclick = () =>
    applyDays(["mon","tue","wed","thu","fri","sat","sun"]);

form.addEventListener("submit", async e => {
    e.preventDefault();

    if (!daysInput.value) {
        output.innerText = "❌ Выбери дни";
        return;
    }

    const data = {
        chat_id: tg.initDataUnsafe.user.id,
        text: text.value,
        time: time.value,
        days: daysInput.value
    };

    const res = await fetch(SERVER_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        output.innerText = "✅ Напоминание создано";
        form.reset();
        selected.clear();
        document.querySelectorAll(".days-grid button").forEach(b => b.classList.remove("active"));
        daysInput.value = "";
    } else {
        output.innerText = "❌ Ошибка";
    }
});

const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

const SERVER_URL = "https://telegram-schedulebot.vercel.app/";

const daysInput = document.getElementById("days");
const output = document.getElementById("output");

let selected = [];

document.querySelectorAll(".day").forEach(el => {
    el.onclick = () => {
        const d = el.dataset.day;
        if (selected.includes(d)) {
            selected = selected.filter(x => x !== d);
            el.classList.remove("active");
        } else {
            selected.push(d);
            el.classList.add("active");
        }
        daysInput.value = selected.join(",");
    };
});

function setDays(arr) {
    selected = arr;
    document.querySelectorAll(".day").forEach(el => {
        el.classList.toggle("active", arr.includes(el.dataset.day));
    });
    daysInput.value = arr.join(",");
}

document.getElementById("weekdays").onclick = () =>
    setDays(["mon","tue","wed","thu","fri"]);

document.getElementById("alldays").onclick = () =>
    setDays(["mon","tue","wed","thu","fri","sat","sun"]);

document.getElementById("submit").onclick = async () => {
    if (!selected.length) {
        output.innerText = "❌ Выбери дни";
        return;
    }

    const msg = `/schedule ${text.value} ${time.value} ${selected.join(",")}`;

    await fetch(SERVER_URL, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            chat_id: tg.initDataUnsafe.user.id,
            text: msg
        })
    });

    output.innerText = "✅ Сохранено";
};
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

let selected = [];
const daysInput = document.getElementById("days");

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

function setDays(arr){
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

document.getElementById("submit").onclick = () => {
    if(!selected.length || !document.getElementById("text").value || !document.getElementById("time").value){
        alert("Заполни все поля и выбери хотя бы один день");
        return;
    }

    const data = {
        text: document.getElementById("text").value,
        time: document.getElementById("time").value,
        days: daysInput.value
    };
    tg.sendData(JSON.stringify(data));
    tg.close();
};
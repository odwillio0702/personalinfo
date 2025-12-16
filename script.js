const BOT_TOKEN = "ТВОЙ_БОТ_ТОКЕН"; 
const CHAT_ID = "ТВОЙ_CHAT_ID"; // можно фиксированный для тебя

const form = document.getElementById("reminderForm");
const output = document.getElementById("output");

form.addEventListener("submit", (e)=>{
    e.preventDefault();
    const text = document.getElementById("text").value;
    const time = document.getElementById("time").value;
    const days = document.getElementById("days").value;

    const msg = `/schedule ${text} ${time} ${days}`;
    fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`,{
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({chat_id: CHAT_ID, text: msg})
    }).then(res=>{
        output.innerText = "✅ Напоминание отправлено боту";
        form.reset();
    }).catch(err=>{
        output.innerText = "❌ Ошибка отправки";
    });
});

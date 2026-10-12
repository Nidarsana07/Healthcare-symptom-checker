function sendMessage() {
    const input = document.getElementById("input");
    const messages = document.getElementById("messages");
    const emptyState = document.getElementById("empty-state");

    if (!input.value) return;

    // Hide empty state when first message is sent
    if (emptyState) emptyState.style.display = "none";

    let msg = input.value;
    messages.innerHTML += `<div class="user">${msg}</div>`;
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg})
    })
    .then(res => res.json())
    .then(data => {
        messages.innerHTML += `
        <div class="bot">
            <b>🩺 ${data.condition}</b><br><br>
            <span class="badge ${data.severity.toLowerCase()}">
                Risk: ${data.severity} (${data.score}%)
            </span><br><br>
            💡 ${data.advice}
        </div>`;
        messages.scrollTop = messages.scrollHeight;
    });
}

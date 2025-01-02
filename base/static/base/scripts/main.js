window.addEventListener("load", () => {
    console.log("hi")
})

let messages = document.getElementById("messages");
let url = `ws://${window.location.host}/ws/socket-server/`;
const ChatSocket = new WebSocket(url);

ChatSocket.addEventListener("message", (e) => {
    let data = JSON.parse(e.data);
    el = document.createElement("div");
    el.innerHTML = data["message"];
    console.log(messages, el);
    messages.appendChild(el);
    console.log("Data: ", data);
});

let form = document.getElementById("form");
form.addEventListener("submit", (e) => {
    e.preventDefault();
    //let message = e.target.value;
    console.log("hi");
    ChatSocket.send(
        JSON.stringify({
            type: "chat",
            message: message,
        })
    );
    form.reset();
});
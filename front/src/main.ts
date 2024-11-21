import { Elm } from "./Main.elm";


const app = Elm.Main.init({
	node: document.getElementById("root"),

});

const ws = new WebSocket(`ws://127.0.0.1:5000/ws`);

app.ports.sendMessage.subscribe(function(message: string) {
	ws.send(message);
});

ws.addEventListener("message", function(event) {
	app.ports.messageReceiver.send(event.data);
});

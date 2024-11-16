import { Elm } from "./Main.elm";

const app = Elm.Main.init({
	node: document.getElementById("root"),
	flags: {
		websocketUrl: "ws://localhost:5000/ws",
	},
});

// Create WebSocket connection
const socket = new WebSocket("ws://localhost:5000/ws");
// Set up ports for WebSocket communication
app.ports?.websocketOut?.subscribe((message: any) => {
	// Handle outgoing messages to WebSocket
	if (socket && socket.readyState === WebSocket.OPEN) {
			socket.send(JSON.stringify(message));
	}
});


socket.onopen = () => {
	console.log("WebSocket connected");
};

socket.onmessage = (event) => {
	// Forward incoming messages to Elm
	if (app.ports?.websocketIn?.send) {
			try {
					const message = JSON.parse(event.data);
					app.ports.websocketIn.send(message);
			} catch (e) {
					console.error("Failed to parse WebSocket message:", e);
			}
	}
};

socket.onerror = (error) => {
	console.error("WebSocket error:", error);
};
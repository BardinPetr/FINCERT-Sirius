var ws = new WebSocket("ws://127.0.0.1:9999");

ws.onopen = function () {
    alert("Connected!")
};

ws.onmessage = function (evt) {
    alert(evt.data);
};

ws.onclose = function () {
    alert('Connection lost')
};


var ws = new WebSocket("ws://0.0.0.0:9999");

ws.onopen = function () {
    alert("Connected!")
};

ws.onmessage = function (evt) {
    alert(evt.data);
};

ws.onclose = function () {
    alert('Connection lost')
};


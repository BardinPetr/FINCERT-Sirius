var ws = new WebSocket("ws://127.0.0.1:9999");

ws.onopen = function () {
    send({"11": 11});
};

ws.onmessage = function (evt) {
};

ws.onclose = function () {
    alert('Connection lost')
};

var enc = function (a) {
    var currentdate = new Date();
    var datetime = currentdate.getDate() + "/"
        + (currentdate.getMonth() + 1) + "/"
        + currentdate.getFullYear() + "@#"
        + currentdate.getHours() + ":"
        + currentdate.getMinutes();
    var x = (datetime + datetime + datetime + datetime).slice(0, 32);
    x = Base64.encode(x);
    var secret = new fernet.Secret(x);
    var token = new fernet.Token({
        secret: secret
    });
    return token.encode("MSG" + JSON.stringify(a));
};

var send = function (a) {
    var x = enc(a);
    ws.send(x);
};


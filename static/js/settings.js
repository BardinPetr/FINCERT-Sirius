let ws = new WebSocket("ws://127.0.0.1:9999"),
    log = console.log;

ws.onopen = function () {
};

ws.onmessage = function (evt) {
};

ws.onclose = function () {
};

let enc = function (a) {
    let currentdate = new Date();
    let datetime = currentdate.getDate() + "/"
        + (currentdate.getMonth() + 1) + "/"
        + currentdate.getFullYear() + "@#"
        + currentdate.getHours() + ":"
        + currentdate.getMinutes();
    let x = (datetime + datetime + datetime + datetime).slice(0, 32);
    x = Base64.encode(x);
    let secret = new fernet.Secret(x);
    let token = new fernet.Token({
        secret: secret
    });
    return token.encode("MSG" + JSON.stringify(a));
};

let send = function (a) {
    let x = enc(a);
    ws.send(x);
};

$(document).ready(function () {
    $("#save").click(() => {
        let data = {
            imaphost: $("#iserver").val(),
            imapport: $("#iport").val(),
            cred: [$("#email").val(), $("#password").val()],
            snifftime: $("#time").val()
        };
        send(data);
        toastr.success("Settings saved on you local computer", "Settings")
    });
});

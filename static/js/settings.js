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
        let ihost_re = new RegExp(/^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/);
        let email_re = new RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
        let pass_re = new RegExp(/^.{6,}$/g);
        if (ihost_re.test(data.imaphost) && email_re.test(data.cred[0]) && pass_re.test(data.cred[1]) &&
            !isNaN(parseInt(data.imapport)) && !isNaN(parseInt(data.snifftime))) {
            send(data);
            toastr.success("Settings saved on you local computer", "Settings")
        } else {
            toastr.error("You didn't enter data correctly", "Settings")
        }
    });
});

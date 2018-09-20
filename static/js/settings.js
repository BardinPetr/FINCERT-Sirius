var sel = function sel(x, y) {
    $("#iserver").val(x);
    $("#iport").val(y);
};

"use strict";

var ws = new WebSocket("ws://127.0.0.1:9999"),
    log = console.log;

ws.onopen = function () {
};

ws.onmessage = function (evt) {
};

ws.onclose = function () {
};

var enc = function enc(a) {
    var currentdate = new Date();
    var datetime = currentdate.getDate() + "/" + (currentdate.getMonth() + 1) + "/" + currentdate.getFullYear() + "@#" + currentdate.getHours() + ":" + currentdate.getMinutes();
    var x = (datetime + datetime + datetime + datetime).slice(0, 32);
    x = Base64.encode(x);
    var secret = new fernet.Secret(x);
    var token = new fernet.Token({
        secret: secret
    });
    return token.encode("MSG" + JSON.stringify(a));
};

var send = function send(a) {
    var x = enc(a);
    ws.send(x);
};

$(document).ready(function () {
    $("#time").val($("#time").val() || "10");
    $("#daysf").val($("#daysf").val() || "10");
    $("#daysm").val($("#daysm").val() || "14");

    var data = [["GMail", "imap.gmail.com", 993], ["Yandex", "imap.yandex.ru", 993],
        ["Yahoo!", "imap.mail.yahoo.com", 993], ["Mail.ru", "imap.mail.ru", 993], ["Rambler", "imap.rambler.ru", 993],
        ["Outlook", "imap-mail.outlook.com", 993]];
    data.forEach(function (i, a, b) {
        $("#imapsel_dd").append("<li><button type=\"button\" class=\"btn btn-link btn-block\" onclick=\"sel('" + i[1] + "', '" + i[2] + "')\">" + i[0] + "</button></li>");
    });

    $("#save").click(function () {
        var mdata = {
            imaphost: $("#iserver").val(),
            imapport: $("#iport").val(),
            cred: [$("#email").val(), $("#password").val()]
        };
        var tdata = {
            snifftime: $("#time").val(),
            filetime: $("#daysf").val(),
            mailtime: $("#daysm").val()
        };
        var pdata = {
            rpath: $("#rootpath").val()
        };
        var ihost_re = new RegExp(/^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/);
        var email_re = new RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
        var pass_re = new RegExp(/^.{6,}$/g);
        var mail_x = ihost_re.test(mdata.imaphost) && email_re.test(mdata.cred[0]) && pass_re.test(mdata.cred[1]) && !isNaN(parseInt(mdata.imapport)) && parseInt(mdata.imapport) > 0,
            time_x = !isNaN(parseInt(tdata.snifftime)) && parseInt(tdata.snifftime) > 0,
            mtime_x = !isNaN(parseInt(tdata.mailtime)) && parseInt(tdata.mailtime) > 0,
            ftime_x = !isNaN(parseInt(tdata.filetime)) && parseInt(tdata.filetime) > 0;
        var ismail = mdata.imapport || mdata.imaphost || mdata.cred[0] || mdata.cred[1];
        var istime = Boolean(tdata.snifftime);
        var istimef = Boolean(tdata.filetime);
        var istimem = Boolean(tdata.mailtime);
        var ispath = Boolean(pdata.rpath);
        tdata.snifftime = parseInt(tdata.snifftime);
        tdata.mailtime = parseInt(tdata.mailtime);
        tdata.filetime = parseInt(tdata.filetime);

        var res = {
            mail: false,
            time: [],
            snifftime: 10,
            mailtime: 14,
            filetime: 10,
            imapport: '',
            imaphost: '',
            rootpath: '',
            cred: ['', '']
        };
        if (ismail) {
            if (mail_x) {
                res = Object.assign(res, mdata);
                res.mail = true;
            } else {
                toastr.error("Данные почты неверно введены", "Настройки");
                return;
            }
        }
        if (istime) {
            if (time_x) {
                res.time.concat('sniff');
                res.snifftime = tdata.snifftime;
            } else {
                toastr.error("Данные времени неверно введены", "Настройки");
                return;
            }
        }
        if (istimef) {
            if (ftime_x) {
                res.time.concat('file');
                res.filetime = tdata.filetime;
            } else {
                toastr.error("Данные времени неверно введены", "Настройки");
                return;
            }
        }
        if (istimem) {
            if (mtime_x) {
                res.time.concat('mail');
                res.mailtime = tdata.mailtime;
            } else {
                toastr.error("Данные времени неверно введены", "Настройки");
                return;
            }
        }
        if (ispath) {
            $.get("exists", {x: Base64.encode(pdata.rpath)}, function (data) {
                if (parseInt(data)) {
                    res.rootpath = pdata.rpath;
                } else {
                    toastr.error("Данные путей неверно введены", "Настройки");
                    return;
                }
                done();
            });
        } else {
            done();
        }

        function done() {
            if (!ismail && !istime && !istimef && !istimem) {
                toastr.error("Данные времени неверно введены", "Настройки");
                return;
            }
            send(res);
            toastr.success("Настройки сохранены на ваш компьютер", "Настройки");
        }
    });
});
const ws = new WebSocket("ws://127.0.0.1:9999"),
    log = console.log;

let format_data = {
    used: [],
    mail: {
        email: [],
        text: []
    },
    net: {
        ip: [],
        url: []
    },
    reg: {
        keys: []
    },
    files: [],
    ram: {
        procs: []
    },
    log: []
};

const append_log = data => {
    $("#logs").html(data + "<br>" + $("#logs").html())
};

Array.prototype.remove = function () {
    let what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};

ws.onopen = function () {
};

ws.onmessage = function (evt) {
    let a = JSON.parse(evt.data.toString());
    if (a.xtype === 2) {
        const text_block = $("#rmodal-body");
        let apnd = "",
            yay = 0;
        if (Object.keys(a).indexOf('file') !== -1) {
            if (Object.keys(a.file).length !== 0) {
                yay++;
                apnd += `<div class="panel panel-default"><div class="panel-heading">Found files: </div><div class="panel-body"><ul class="list-group">`;
                Object.keys(a.file).forEach(function (key) {
                    apnd += `<li class="list-group-item list-group-item-danger">${key} at ${a.file[key]}</li>`;
                });
                apnd += `</ul></div></div>`;
            }
        }
        if (Object.keys(a).indexOf('mail') !== -1) {
            if (a.mail.length !== 0) {
                yay++;
                apnd += `<div class="panel panel-default"><div class="panel-heading">Found mails: </div><div class="panel-body"><ul class="list-group">`;
                a.mail.forEach(function (mail) {
                    apnd += `<li class="list-group-item list-group-item-danger">Mail from ${mail.from} at ${mail.date}</li>`;
                });
                apnd += `</ul></div></div>`;
            }
        }
        if (Object.keys(a).indexOf('net') !== -1) {
            if (a.net['format'].length !== 0) {
                yay++;
                apnd += `<div class="panel panel-default"><div class="panel-heading">Found network requests: </div><div class="panel-body"><ul class="list-group">`;
                a.net['format'].forEach(function (elem) {
                    apnd += `<li class="list-group-item list-group-item-danger">${elem}</li>`;
                });
                apnd += `</ul></div></div>`;
            }
        }
        if (Object.keys(a).indexOf('reg') !== -1) {
            if (a.reg.length !== 0) {
                yay++;
                apnd += `<div class="panel panel-default"><div class="panel-heading">Found registry records: </div><div class="panel-body"><ul class="list-group">`;
                a.reg.forEach(function (elem) {
                    apnd += `<li class="list-group-item list-group-item-danger">${elem}</li>`;
                });
                apnd += `</ul></div></div>`;
            }
        }
        if (Object.keys(a).indexOf('ram') !== -1) {
            if (a.ram.length !== 0) {
                yay++;
                apnd += `<div class="panel panel-default"><div class="panel-heading">Found running processes: </div><div class="panel-body"><ul class="list-group">`;
                a.ram.forEach(function (elem) {
                    apnd += `<li class="list-group-item list-group-item-danger">${elem}</li>`;
                });
                apnd += `</ul></div></div>`;
            }
        }
        text_block.html(apnd);
        $("#results_modal").modal();
        if (yay === 0) {
            $("#yay").hide();
            text_block.append(`
                    <div id="yay" class="alert alert-success">
                        <strong>YAY!</strong> There isn't any IOCs in your system!!!
                    </div>`);
            $("#yay").fadeIn(1000);
        }
    } else if (a.xtype === 1) {
        toastr[a.color](a.text, a.title);
        append_log(`[${a.title}] ${a.text}`);
    } else if (a.xtype === 0) {
        append_log(a.data);
    }
    a = {};
};

ws.onclose = function () {
};

const format_litxt = (type, name) => {
    return Base64.toBase64(`li${type}txt_${name}`).replace(/\W/g, "0");
};

function del_elem(name, id, type) {
    type = parseInt(type);
    $("#" + format_litxt(type, name)).remove();
    let x = [format_data.files, format_data.mail.email, format_data.mail.text, format_data.net.ip, format_data.net.url,
        format_data.reg.keys, format_data.ram.procs, format_data.log][type].filter(y => y.disp !== name);
    switch (type) {
        case 0:
            format_data.files = x;
            break;
        case 1:
            format_data.mail.email = x;
            break;
        case 2:
            format_data.mail.text = x;
            break;
        case 3:
            format_data.net.ip = x;
            break;
        case 4:
            format_data.net.url = x;
            break;
        case 5:
            format_data.reg.keys = x;
            break;
        case 6:
            format_data.ram.procs = x;
            break;
        case 7:
            format_data.log = x;
            break;
    }
}

const file_item_tmpl = (name, id, type) => {
    let xname = format_litxt(type, name);
    return `<li id="${xname}" class="list-group-item">${name}<span class="badge">
            <i class="fas fa-times" onclick='del_elem("${name}", "${id}", "${type}");'></i></span></li>`;
};

$(document).ready(function () {
    const file_objs = ['name', 'size', 'sha1', 'sha256', 'md5'].map((x, i, a) => {
        return $("#file_" + x)
    });

    $('#file_add').click(function () {
        let cur = {
            name: file_objs[0].val(),
            size: parseInt(file_objs[1].val()),
            sha1: file_objs[2].val(),
            sha256: file_objs[3].val(),
            md5: file_objs[4].val()
        };
        if (cur.name && cur.size && cur.md5 && cur.sha1 && cur.sha256) {
            format_data.files = format_data.files.concat({disp: cur.name, norm: cur});
            file_objs.map((x, i, a) => {
                x.val('')
            });
            $('#file_list').prepend(file_item_tmpl(cur.name, format_data.files.length - 1, 0));
            toastr.info("Added successfully", "PARAMS");
        } else {
            toastr.warning("Not all fields are carefully entered", "PARAMS");
        }
    });

    $('#mail_addr_add').click(function () {
        let c = $("#mail_addr_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.mail.email = format_data.mail.email.concat({disp: cur, norm: cur});
            $('#mail_addr_list').prepend(file_item_tmpl(cur, format_data.mail.email.length - 1, 1));
            toastr.info("Added successfully", "PARAMS");
        } else {
            toastr.warning("Not all fields are carefully entered", "PARAMS");
        }
    });

    $('#mail_txt_add').click(function () {
        let c = $("#mail_txt_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            let displaytxt = cur.slice(0, 8) + '...';
            format_data.mail.text = format_data.mail.text.concat({disp: displaytxt, norm: cur});
            $('#mail_txt_list').prepend(file_item_tmpl(displaytxt, format_data.mail.text.length - 1, 2));
            toastr.info("Added successfully", "PARAMS");
        } else {
            toastr.warning("Not all fields are carefully entered", "PARAMS");
        }
    });

    $('#net_ip_add').click(function () {
        let c = $("#net_ip_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.net.ip = format_data.net.ip.concat({disp: cur, norm: cur});
            $('#net_ip_list').prepend(file_item_tmpl(cur, format_data.net.ip.length - 1, 3));
            toastr.info("Added successfully", "PARAMS");
        } else {
            toastr.warning("Not all fields are carefully entered", "PARAMS");
        }
    });

    $('#net_url_add').click(function () {
        let c = $("#net_url_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.net.url = format_data.net.url.concat({disp: cur, norm: cur});
            $('#net_url_list').prepend(file_item_tmpl(cur, format_data.net.url.length - 1, 4));
            toastr.info("Added successfully", "PARAMS");
        } else {
            toastr.warning("Not all fields are carefully entered", "PARAMS");
        }
    });

    $('#reg_add').click(function () {
        let k = $("#reg_key"),
            v = $("#reg_val");
        let cur = {key: k.val(), val: v.val()};
        k.val('');
        v.val('');
        if (cur.key && cur.val) {
            let disp = cur.key.split(0, 30) + '...';
            format_data.reg.keys = format_data.reg.keys.concat({disp: disp, norm: cur});
            $('#reg_list').prepend(file_item_tmpl(disp, format_data.reg.keys.length - 1, 5));
            toastr.info("Added successfully", "PARAMS");
        } else {
            toastr.warning("Not all fields are carefully entered", "PARAMS");
        }
    });

    $('#ram_add').click(function () {
        let c = $("#ram_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.ram.procs = format_data.ram.procs.concat({disp: cur, norm: cur});
            $('#ram_list').prepend(file_item_tmpl(cur, format_data.ram.procs.length - 1, 6));
            toastr.info("Added successfully", "PARAMS");
        } else {
            toastr.warning("Not all fields are carefully entered", "PARAMS");
        }
    });

    $('#log_add').click(function () {
        let c = $("#log_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.log = format_data.log.concat({disp: cur, norm: cur});
            $('#log_list').prepend(file_item_tmpl(cur, format_data.log.length - 1, 7));
            toastr.info("Added successfully", "PARAMS");
        } else {
            toastr.warning("Not all fields are carefully entered", "PARAMS");
        }
    });

    let panel_names = ["files", "mail", "net", "reg", "ram", "log"];
    panel_names.map((name, index, arr) => {
        $(`#panel_${name}`).hide();
        $(`#${name}_cb`).on('click', function () {
            if ($(`#${name}_cb`).prop('checked')) {
                $('#zeropanel').fadeOut(500);
                format_data.used = format_data.used.concat(name);
                $(`#panel_${name}`).fadeIn(1000);
            } else {
                format_data.used = format_data.used.remove(name);
                $(`#panel_${name}`).fadeOut(1000);
                if (format_data.used.length === 0) {
                    $('#zeropanel').fadeIn(500);
                }
            }
        });
    });

    $('#btn_start').click(() => {
        if (format_data.used.length === 0) {
            toastr.warning("No modules selected", "SCAN");
        } else {
            ws.send("NOTENC:::START:::" + JSON.stringify(format_data));
        }
    });

    $('#btn_stop').click(() => {
        ws.send("NOTENC:::STOP")
    });

    append_log('[SYSTEM] WEB init finished');
});
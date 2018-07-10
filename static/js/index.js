const ws = new WebSocket("ws://127.0.0.1:9999"),
    log = console.log;

let format_data = {
    used: [],
    mailaddrs: [],
    mailtxts: [],
    net_urls: [],
    net_ips: [],
    regkeys: [],
    files: [],
    procs: [],
    logs: []
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
    alert(evt.data);
};

ws.onclose = function () {
};

const format_litxt = (type, name) => {
    return Base64.toBase64(`li${type}txt_${name}`).replace(/\W/g, "0");
};

function del_elem(name, id, type) {
    type = parseInt(type);
    $("#" + format_litxt(type, name)).remove();
    x = [format_data.files, format_data.mailaddrs, format_data.mailtxts, format_data.net_ips, format_data.net_urls, format_data.regkeys, format_data.procs, format_data.logs][type].filter(y => y.disp !== name);
    switch (type) {
        case 0:
            format_data.files = x;
            break;
        case 1:
            format_data.mailaddrs = x;
            break;
        case 2:
            format_data.mailtxts = x;
            break;
        case 3:
            format_data.net_ips = x;
            break;
        case 4:
            format_data.net_urls = x;
            break;
        case 5:
            format_data.regkeys = x;
            break;
        case 6:
            format_data.procs = x;
            break;
        case 7:
            format_data.logs = x;
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
            size: file_objs[1].val(),
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
        }
    });

    $('#mail_addr_add').click(function () {
        let c = $("#mail_addr_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.mailaddrs = format_data.mailaddrs.concat({disp: cur, norm: cur});
            $('#mail_addr_list').prepend(file_item_tmpl(cur, format_data.mailaddrs.length - 1, 1));
        }
    });

    $('#mail_txt_add').click(function () {
        let c = $("#mail_txt_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            let displaytxt = cur.slice(0, 8) + '...';
            format_data.mailtxts = format_data.mailtxts.concat({disp: displaytxt, norm: cur});
            $('#mail_txt_list').prepend(file_item_tmpl(displaytxt, format_data.mailtxts.length - 1, 2));
        }
    });

    $('#net_ip_add').click(function () {
        let c = $("#net_ip_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.net_ips = format_data.net_ips.concat({disp: cur, norm: cur});
            $('#net_ip_list').prepend(file_item_tmpl(cur, format_data.net_ips.length - 1, 3));
        }
    });

    $('#net_url_add').click(function () {
        let c = $("#net_url_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.net_urls = format_data.net_urls.concat({disp: cur, norm: cur});
            $('#net_url_list').prepend(file_item_tmpl(cur, format_data.net_urls.length - 1, 4));
        }
    });

    $('#reg_add').click(function () {
        let c = $("#reg_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.regkeys = format_data.regkeys.concat({disp: cur, norm: cur});
            $('#reg_list').prepend(file_item_tmpl(cur, format_data.regkeys.length - 1, 5));
        }
    });

    $('#ram_add').click(function () {
        let c = $("#ram_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.procs = format_data.procs.concat({disp: cur, norm: cur});
            $('#ram_list').prepend(file_item_tmpl(cur, format_data.procs.length - 1, 6));
        }
    });

    $('#log_add').click(function () {
        let c = $("#log_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            format_data.logs = format_data.logs.concat({disp: cur, norm: cur});
            $('#log_list').prepend(file_item_tmpl(cur, format_data.logs.length - 1, 7));
        }
    });

    let cbs = ["format_data.files", "mail", "net", "reg", "ram", "log"];
    cbs.map((x, n, a) => {
        $(`#panel_${x}`).hide();
        $(`#${x}_cb`).on('click', function () {
            if ($(`#${x}_cb`).prop('checked')) {
                $('#zeropanel').fadeOut(500);
                format_data.used = format_data.used.concat(x);
                $(`#panel_${x}`).fadeIn(1000);
            } else {
                format_data.used = format_data.used.remove(x);
                $(`#panel_${x}`).fadeOut(1000);
                if (format_data.used.length === 0) {
                    $('#zeropanel').fadeIn(500);
                }
            }
        });

    });
});


const gen_std_datapack = () => format_data;
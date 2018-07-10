const ws = new WebSocket("ws://127.0.0.1:9999"),
    log = console.log;

let mailaddrs = [];
let mailtxts = [];
let net_urls = [];
let net_ips = [];
let regkeys = [];
let files = [];
let procs = [];
let logs = [];


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
    x = [files, mailaddrs, mailtxts, net_ips, net_urls, regkeys, procs, logs][type].filter(y => y.disp !== name);
    switch (type) {
        case 0:
            files = x;
            break;
        case 1:
            mailaddrs = x;
            break;
        case 2:
            mailtxts = x;
            break;
            regkeys
        case 3:
            net_ips = x;
            break;
        case 4:
            net_urls = x;
            break;
        case 5:
            regkeys = x;
            break;
        case 6:
            procs = x;
            break;
        case 7:
            logs = x;
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
            files = files.concat({disp: cur.name, norm: cur});
            file_objs.map((x, i, a) => {
                x.val('')
            });
            $('#file_list').prepend(file_item_tmpl(cur.name, files.length - 1, 0));
        }
    });

    $('#mail_addr_add').click(function () {
        let c = $("#mail_addr_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            mailaddrs = mailaddrs.concat({disp: cur, norm: cur});
            $('#mail_addr_list').prepend(file_item_tmpl(cur, mailaddrs.length - 1, 1));
        }
    });

    $('#mail_txt_add').click(function () {
        let c = $("#mail_txt_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            let displaytxt = cur.slice(0, 8) + '...';
            mailtxts = mailtxts.concat({disp: displaytxt, norm: cur});
            $('#mail_txt_list').prepend(file_item_tmpl(displaytxt, mailtxts.length - 1, 2));
        }
    });

    $('#net_ip_add').click(function () {
        let c = $("#net_ip_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            net_ips = net_ips.concat({disp: cur, norm: cur});
            $('#net_ip_list').prepend(file_item_tmpl(cur, net_ips.length - 1, 3));
        }
    });

    $('#net_url_add').click(function () {
        let c = $("#net_url_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            net_urls = net_urls.concat({disp: cur, norm: cur});
            $('#net_url_list').prepend(file_item_tmpl(cur, net_urls.length - 1, 4));
        }
    });

    $('#reg_add').click(function () {
        let c = $("#reg_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            regkeys = regkeys.concat({disp: cur, norm: cur});
            $('#reg_list').prepend(file_item_tmpl(cur, regkeys.length - 1, 5));
        }
    });

    $('#ram_add').click(function () {
        let c = $("#ram_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            procs = procs.concat({disp: cur, norm: cur});
            $('#ram_list').prepend(file_item_tmpl(cur, procs.length - 1, 6));
        }
    });

    $('#log_add').click(function () {
        let c = $("#log_inp");
        let cur = c.val();
        c.val('');
        if (cur) {
            logs = logs.concat({disp: cur, norm: cur});
            $('#log_list').prepend(file_item_tmpl(cur, logs.length - 1, 7));
        }
    });
});
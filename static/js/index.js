'use strict';

var loc = window.location.hostname,
    log = console.log;

var format_data = {
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

var resmod_goup = function resmod_goup() {
    $('#results_modal').animate({ scrollTop: 0 }, 'slow');
};

var format_litxt = function format_litxt(type, name) {
    return Base64.toBase64('li' + type + 'txt_' + name).replace(/\W/g, "0");
};

var file_item_tmpl = function file_item_tmpl(name, id, type) {
    var xname = format_litxt(type, name);
    return '<li id="' + xname + '" class="list-group-item">' + name + '<span class="badge">\n            <i class="fas fa-times" onclick=\'del_elem("' + name + '", "' + id + '", "' + type + '");\'></i></span></li>';
};

function del_elem(name, id, type) {
    type = parseInt(type);
    $("#" + format_litxt(type, name)).remove();
    var x = [format_data.files, format_data.mail.email, format_data.mail.text, format_data.net.ip, format_data.net.url, format_data.reg.keys, format_data.ram.procs, format_data.log][type].filter(function (y) {
        return y.disp !== name;
    });
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

var reset_all = function reset_all() {
    window.location.replace('http://' + loc + ':8080/');
};

$(document).ready(function () {
    var ws = new WebSocket('ws://' + loc + ':9999');
    $("#fs_wrapper").fadeOut(1);

    var indicate_running = function indicate_running(state) {
        if (state) {
            $("#loading_gif").fadeIn(4000);
            start_btn.prop("disabled", true);
            stop_btn.prop("disabled", false);
        } else {
            $("#loading_gif").fadeOut(4000);
            stop_btn.prop("disabled", true);
            start_btn.prop("disabled", false);
        }
    };

    var append_log = function append_log(data) {
        $("#logs").html(data + "<br>" + $("#logs").html());
    };

    $("#gotop_fab").click(function () {
        window.scroll({
            top: 0,
            left: 0,
            behavior: 'smooth'
        });
    });

    window.onscroll = function () {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            $("#gotop_fab").css("display", "block");
        } else {
            $("#gotop_fab").css("display", "none");
        }
    };

    Array.prototype.remove = function () {
        var what = void 0,
            a = arguments,
            L = a.length,
            ax = void 0;
        while (L && this.length) {
            what = a[--L];
            while ((ax = this.indexOf(what)) !== -1) {
                this.splice(ax, 1);
            }
        }
        return this;
    };

    var addh_file = function addh_file(cur) {
        var disp = cur.name || cur.sha256 || cur.sha1 || cur.md5 || cur.size;
        disp = disp.slice(0, 30) + '...';
        format_data.files = format_data.files.concat({ disp: disp, norm: cur });
        $('#file_list').prepend(file_item_tmpl(disp, format_data.files.length - 1, 0));
    };
    var addh_mail_a = function addh_mail_a(cur) {
        format_data.mail.email = format_data.mail.email.concat({ disp: cur, norm: cur });
        $('#mail_addr_list').prepend(file_item_tmpl(cur, format_data.mail.email.length - 1, 1));
    };
    var addh_mail_t = function addh_mail_t(cur) {
        var displaytxt = cur.slice(0, 20) + '...';
        format_data.mail.text = format_data.mail.text.concat({ disp: displaytxt, norm: cur });
        $('#mail_txt_list').prepend(file_item_tmpl(displaytxt, format_data.mail.text.length - 1, 2));
    };
    var addh_net_i = function addh_net_i(cur) {
        format_data.net.ip = format_data.net.ip.concat({ disp: cur, norm: cur });
        $('#net_ip_list').prepend(file_item_tmpl(cur, format_data.net.ip.length - 1, 3));
    };
    var addh_net_u = function addh_net_u(cur) {
        format_data.net.url = format_data.net.url.concat({ disp: cur, norm: cur });
        $('#net_url_list').prepend(file_item_tmpl(cur, format_data.net.url.length - 1, 4));
    };
    var addh_reg = function addh_reg(cur) {
        var disp = cur.key.split(0, 20) + '...';
        format_data.reg.keys = format_data.reg.keys.concat({ disp: disp, norm: cur });
        $('#reg_list').prepend(file_item_tmpl(disp, format_data.reg.keys.length - 1, 5));
    };
    var addh_ram_p = function addh_ram_p(cur) {
        format_data.ram.procs = format_data.ram.procs.concat({ disp: cur, norm: cur });
        $('#ram_list').prepend(file_item_tmpl(cur, format_data.ram.procs.length - 1, 6));
    };
    var addh_log = function addh_log(cur) {
        format_data.log = format_data.log.concat({ disp: cur, norm: cur });
        $('#log_list').prepend(file_item_tmpl(cur, format_data.log.length - 1, 7));
    };

    ws.onopen = function () {
        ws.send("NOTENC:::GETSTIX");
    };

    ws.onmessage = function (evt) {
        var a = JSON.parse(evt.data.toString());
        if (a.xtype === 4) {
            indicate_running(true);
        } else if (a.xtype === 3) {
            if (a.used.length !== 0) {
                format_data.used = a.used;
                $('#zeropanel').fadeOut(500);
                a.used.forEach(function (elem, x, y) {
                    $('#panel_' + elem).show();
                    $('#' + elem + '_cb').prop("checked", true);
                    switch (elem) {
                        case 'files':
                            {
                                a.files.forEach(function (i, x0, z0) {
                                    addh_file(i);
                                });
                                break;
                            }
                        case 'net':
                            {
                                a.net.ip.forEach(function (i, x0, z0) {
                                    addh_net_i(i);
                                });
                                a.net.url.forEach(function (i, x0, z0) {
                                    addh_net_u(i);
                                });
                                break;
                            }
                        case 'mail':
                            {
                                a.mail.email.forEach(function (i, x0, z0) {
                                    addh_mail_a(i);
                                });
                                break;
                            }
                    }
                });
            }
        } else if (a.xtype === 2) {
            indicate_running(false);
            var text_block = $("#rmodal-body");
            var apnd = "",
                yay = 0;
            if (Object.keys(a).indexOf('file') !== -1) {
                if (Object.keys(a.file).length !== 0) {
                    yay++;
                    apnd += '<div class="panel panel-default"><div class="panel-heading">\u041D\u0430\u0439\u0434\u0435\u043D\u043D\u044B\u0435 \u0438\u043D\u0434\u0438\u043A\u0430\u0442\u043E\u0440\u044B \u0444\u0430\u0439\u043B\u043E\u0432: </div><div class="panel-body"><ul class="list-group">';
                    Object.keys(a.file).forEach(function (key) {
                        apnd += '<li class="list-group-item list-group-item-danger">' + key + ' at ' + a.file[key] + '</li>';
                    });
                    apnd += '</ul></div></div>';
                }
            }
            if (Object.keys(a).indexOf('mail') !== -1) {
                if (a.mail.length !== 0) {
                    yay++;
                    apnd += '<div class="panel panel-default"><div class="panel-heading">\u041D\u0430\u0439\u0434\u0435\u043D\u043D\u044B\u0435 \u0438\u043D\u0434\u0438\u043A\u0430\u0442\u043E\u0440\u044B \u0432 \u043F\u043E\u0447\u0442\u0435: </div><div class="panel-body"><ul class="list-group">';
                    a.mail.forEach(function (mail) {
                        apnd += '<li class="list-group-item list-group-item-danger">Mail from ' + mail.from + ' at ' + mail.date + '</li>';
                    });
                    apnd += '</ul></div></div>';
                }
            }
            if (Object.keys(a).indexOf('net') !== -1) {
                if (a.net.length !== 0) {
                    yay++;
                    apnd += '<div class="panel panel-default"><div class="panel-heading">\u041D\u0430\u0439\u0434\u0435\u043D\u043D\u044B\u0435 \u0438\u043D\u0434\u0438\u043A\u0430\u0442\u043E\u0440\u044B \u0432 \u0441\u0435\u0442\u0438: </div><div class="panel-body"><ul class="list-group">';
                    var i = 0;
                    a.net.forEach(function (elem) {
                        var cnt = elem[1].length;
                        apnd += '<li class="list-group-item list-group-item-danger"><strong><p data-toggle="collapse" data-target="#' + i + '">' + elem[0] + '<span class="btn btn-primary btn-sm badge" data-toggle="collapse" data-target="#' + i + '">' + cnt + '<i style="margin-left: 5px" class="fas fa-arrow-circle-down"></i></span></p></strong><div id="' + i + '" class="collapse"><ul class="list-group">';
                        elem[1].forEach(function (x) {
                            apnd += '<li class="list-group-item list-group-item-warning">' + x + '</li>';
                        });
                        apnd += '</ul><button class="btn btn-info btn-block" data-toggle="collapse" data-target="#' + i + '" onclick="resmod_goup()"><i class="fas fa-arrow-circle-up"></i></button></div></li>';
                        i++;
                    });
                    apnd += '</ul></div></div>';
                }
            }
            if (Object.keys(a).indexOf('reg') !== -1) {
                if (a.reg.length !== 0) {
                    yay++;
                    apnd += '<div class="panel panel-default"><div class="panel-heading">\u041D\u0430\u0439\u0434\u0435\u043D\u043D\u044B\u0435 \u0438\u043D\u0434\u0438\u043A\u0430\u0442\u043E\u0440\u044B \u0432 \u0440\u0435\u0435\u0441\u0442\u0440\u0435: </div><div class="panel-body"><ul class="list-group">';
                    a.reg.forEach(function (elem) {
                        apnd += '<li class="list-group-item list-group-item-danger">' + elem + '</li>';
                    });
                    apnd += '</ul></div></div>';
                }
            }
            if (Object.keys(a).indexOf('ram') !== -1) {
                if (a.ram.length !== 0) {
                    yay++;
                    apnd += '<div class="panel panel-default"><div class="panel-heading">\u041D\u0430\u0439\u0434\u0435\u043D\u043D\u044B\u0435 \u0437\u0430\u043F\u0443\u0449\u0435\u043D\u043D\u044B\u0435 \u043F\u0440\u043E\u0446\u0435\u0441\u0441\u044B: </div><div class="panel-body"><ul class="list-group">';
                    a.ram.forEach(function (elem) {
                        apnd += '<li class="list-group-item list-group-item-danger">' + elem + '</li>';
                    });
                    apnd += '</ul></div></div>';
                }
            }
            text_block.html(apnd);
            $("#results_modal").modal();
            if (yay === 0) {
                $("#yay").hide();
                text_block.append('\n                    <div id="yay" class="alert alert-success">\n                        \u0412 \u0432\u0430\u0448\u0435\u0439 \u0441\u0438\u0441\u0442\u0435\u043C\u0435 \u043D\u0435 \u043D\u0430\u0439\u0434\u0435\u043D\u044B \u0438\u043D\u0434\u0438\u043A\u0430\u0442\u043E\u0440\u044B \u043A\u043E\u043C\u043F\u0440\u043E\u043C\u0435\u0442\u0430\u0446\u0438\u0438!!!\n                    </div>');
                $("#yay").fadeIn(1000);
            }
        } else if (a.xtype === 1) {
            toastr[a.color](a.text, a.title);
            append_log('[' + a.title + '] ' + a.text);
            if (a.color === 'error') indicate_running(false);
        } else if (a.xtype === 0) {
            append_log(a.data);
        }
        a = {};
    };

    ws.onclose = function () {};

    $('[data-toggle="tooltip"]').tooltip();
    $("#loading_gif").hide();

    $("#power_off").click(function () {
        ws.send("NOTENC:::POWEROFF");
        indicate_running(false);
        start_btn.prop("disabled", true);
        $("#fs_wrapper").css('background', '#111111 url("/static/images/disconnected.png") no-repeat center center');
        $("#all").fadeOut(1000);
        setTimeout(function () {
            $("#fs_wrapper").fadeIn(4000);
        }, 1000);
    });

    var start_btn = $('#btn_start'),
        stop_btn = $('#btn_stop');

    var file_objs = ['name', 'size', 'sha1', 'sha256', 'md5'].map(function (x, i, a) {
        return $("#file_" + x);
    });

    $('#file_add').click(function () {
        var cur = {
            name: file_objs[0].val(),
            size: parseInt(file_objs[1].val()),
            sha1: file_objs[2].val(),
            sha256: file_objs[3].val(),
            md5: file_objs[4].val()
        };
        if (cur.name && cur.size && cur.md5 && cur.sha1 && cur.sha256) {
            file_objs.map(function (x, i, a) {
                x.val('');
            });
            addh_file(cur);
            toastr.info("Успешно добавлен", "Параметры");
        } else {
            toastr.warning("Не все поля заполнены корректно", "Параметры");
        }
    });

    $('#mail_addr_add').click(function () {
        var c = $("#mail_addr_inp");
        var cur = c.val();
        c.val('');
        if (cur) {
            addh_mail_a(cur);
            toastr.info("Успешно добавлен", "Параметры");
        } else {
            toastr.warning("Не все поля заполнены корректно", "Параметры");
        }
    });

    $('#mail_txt_add').click(function () {
        var c = $("#mail_txt_inp");
        var cur = c.val();
        c.val('');
        if (cur) {
            addh_mail_t(cur);
            toastr.info("Успешно добавлен", "Параметры");
        } else {
            toastr.warning("Не все поля заполнены корректно", "Параметры");
        }
    });

    $('#net_ip_add').click(function () {
        var c = $("#net_ip_inp");
        var cur = c.val();
        c.val('');
        if (cur) {
            addh_net_i(cur);
            toastr.info("Успешно добавлен", "Параметры");
        } else {
            toastr.warning("Не все поля заполнены корректно", "Параметры");
        }
    });

    $('#net_url_add').click(function () {
        var c = $("#net_url_inp");
        var cur = c.val();
        c.val('');
        if (cur) {
            addh_net_u(cur);
            toastr.info("Успешно добавлен", "Параметры");
        } else {
            toastr.warning("Не все поля заполнены корректно", "Параметры");
        }
    });

    $('#reg_add').click(function () {
        var k = $("#reg_key"),
            v = $("#reg_val");
        var cur = { key: k.val(), val: v.val() };
        k.val('');
        v.val('');
        if (cur.key && cur.val) {
            addh_reg(cur);
            toastr.info("Успешно добавлен", "Параметры");
        } else {
            toastr.warning("Не все поля заполнены корректно", "Параметры");
        }
    });

    $('#ram_add').click(function () {
        var c = $("#ram_inp");
        var cur = c.val();
        c.val('');
        if (cur) {
            addh_ram_p(cur);
            toastr.info("Успешно добавлен", "Параметры");
        } else {
            toastr.warning("Не все поля заполнены корректно", "Параметры");
        }
    });

    $('#log_add').click(function () {
        var c = $("#log_inp");
        var cur = c.val();
        c.val('');
        if (cur) {
            addh_log(cur);
            toastr.info("Успешно добавлен", "Параметры");
        } else {
            toastr.warning("Не все поля заполнены корректно", "Параметры");
        }
    });

    var panel_names = ["files", "mail", "net", "reg", "ram", "log"];
    panel_names.map(function (name, index, arr) {
        $('#panel_' + name).hide();
        $('#' + name + '_cb').on('click', function () {
            if ($('#' + name + '_cb').prop('checked')) {
                $('#zeropanel').fadeOut(500);
                format_data.used = format_data.used.concat(name);
                $('#panel_' + name).fadeIn(1000);
            } else {
                format_data.used = format_data.used.remove(name);
                $('#panel_' + name).fadeOut(1000);
                if (format_data.used.length === 0) {
                    $('#zeropanel').fadeIn(500);
                }
            }
        });
    });

    indicate_running(false);
    start_btn.click(function () {
        if (format_data.used.length === 0) {
            toastr.warning("Ни один из модулей поиска не выбран", "Сканирование");
        } else {
            ws.send("NOTENC:::START:::" + JSON.stringify(format_data));
        }
    });

    stop_btn.click(function () {
        indicate_running(false);
        ws.send("NOTENC:::STOP");
    });
    append_log('[СИСТЕМА] ВЕБ-часть загружена');
});
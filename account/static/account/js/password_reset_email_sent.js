/*
Schoolmate - school management system
Copyright (C) 2018-2021  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

//
// General
//
var URL_LOGIN = "/profile/login/";

//
// Widget description
//
var sentForm = {
    view: "form", name: "password_reset_email_sent_form", width: 660,
    id: "password_reset_email_sent_form", elements: [
        {
            view: "label", align: "center",
            label: gettext("Password reset confirmation has been sent to your e-mail"),
        },
        {
            view: "button", value: gettext("Back to login page"),
            name: "back_to_login_btn", id: "back_to_login_btn",
            href: URL_LOGIN, click: function() {
                webix.send(this.config.href, {}, "GET")
            },
            align: "center", minWidth: 300, width: 310
        }
    ]
};

//
// UI init
//
webix.ui({
     id: "auth_layout", type: "space", container: "div_main", rows: [{
        align: "center,middle", body: {
            type: "space", borderless: true, rows: [sentForm]
        }
    }]
});

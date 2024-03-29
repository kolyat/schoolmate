/*
Schoolmate - school management system
Copyright (C) 2018-2022  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>

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
var resetCompleteForm = {
    view: "form", name: "password_reset_complete_form", minWidth: 330,
    id: "password_reset_complete_form", maxWidth: 400, elements: [
        {
            view: "template", autoheight: true, borderless: true,
            css: {"text-align": "center"},
            template: gettext("Password reset complete")
        },
        {
            view: "button", value: gettext("Back to login page"),
            name: "back_to_login_btn", id: "back_to_login_btn",
            href: URL_LOGIN, click: function() {
                webix.send(this.config.href, {}, "GET")
            },
            align: "center", minWidth: 260, width: 280
        }
    ]
};

var startLayout = {
     view: "layout", id: "start_layout", type: "space",
     responsive: true, borderless: true, rows: [{
        align: "center,middle", body: {
            view: "layout", type: "space", responsive: true, borderless: true,
            rows: [resetCompleteForm]
        }
    }]
};

//
// UI init
//
webix.ui(startLayout, base_layout, b_body);

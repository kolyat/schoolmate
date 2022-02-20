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
var URL_PASSWD_RESET = "/profile/password_reset/";

//
// Widget description
//
var formHeader = {
    view: "template", type: "header", name: "login_header",
    template: gettext("Log in to system")
};
var loginForm = {
    view: "form", name: "login_form", id: "login_form",
    minWidth: 270, maxWidth: 360, elements: [
        {
            view: "text", type: "text", value: csrfToken,
            name: "csrfmiddlewaretoken", id: "csrfmiddlewaretoken",
            hidden: true
        },
        {
            view: "text", placeholder: gettext("Username"),
            name: "username", id: "username",
            invalidMessage: gettext("Username can not be empty"),
        },
        {
            view: "text", placeholder: gettext("Password"),
            type: "password", name: "password", id: "password",
            invalidMessage: gettext("Password can not be empty")
        },
        {
            view: "button", value: gettext("Log in"),
            type: "form", name: "login_btn", id: "login_btn",
            align: "center", minWidth: 130, width: 140
        },
    ],
    rules: {
        "username": webix.rules.isNotEmpty,
        "password": webix.rules.isNotEmpty
    }
};
var passwdButton = {
    view: "button", value: gettext("Forgot password"),
    name: "forgot_password_btn", id: "forgot_password_btn",
    href: URL_PASSWD_RESET,
    click: function() { webix.send(this.config.href, {}, "GET"); },
    minWidth: 165, width: 170, minHeight: 28, height: 30
};

var startLayout = {
    view: "layout", id: "start_layout", type: "space",
    responsive: true, borderless: true, rows: [{
        align: "center,middle", body: {
            view: "layout", type: "space", responsive: true, borderless: true,
            rows: [
                formHeader,
                loginForm,
                passwdButton
            ]
        }
    }]
};

//
// UI init
//
webix.ui(startLayout, base_layout, b_body);

var login_form = $$("login_form");

//
// UI logic
//
function postLoginForm() {
    var loginURL = window.location.href;
    if (login_form.validate()) {
        webix.ajax().post(loginURL, login_form.getValues(),
            function(text, data, xhr) {
                if (xhr["responseURL"] !== loginURL) {
                    webix.send(xhr["responseURL"], {}, "GET");
                } else {
                    webix.message({
                        text: gettext("Wrong username/password"),
                        type: "error",
                        expire: messageExpireTime,
                        id: "wrong_credentials_msg"
                    });
                }
            }
        )
    }
}

//
// Event handling
//
login_form.attachEvent("onSubmit", postLoginForm);
login_form.elements["login_btn"].attachEvent("onItemClick", postLoginForm);

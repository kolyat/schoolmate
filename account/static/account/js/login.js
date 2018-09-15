/*
Schoolmate - school management system
Copyright (C) 2018  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>

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

webix.ui({
    align: "center,middle",
    body: {
        rows: [
            {
                view: "template", type: "header", name: "login_header",
                template: gettext("Log in to system")
            },
            {
                view: "form", name: "login_form", id: "login_form", elements: [
                    {
                        view: "text", type: "text", value: csrfToken,
                        name: "csrfmiddlewaretoken", id: "csrfmiddlewaretoken",
                        hidden: true
                    },
                    {
                        view: "text", placeholder: gettext("Username"),
                        name: "username", id: "username",
                        invalidMessage: gettext("Username can not be empty")
                    },
                    {
                        view: "text", placeholder: gettext("Password"),
                        type: "password",
                        name: "password", id: "password",
                        invalidMessage: gettext("Password can not be empty")
                    },
                    {
                        view: "button", value: gettext("Log in"),
                        type: "form", name: "login_btn", id: "login_btn",
                        align: "center", minWidth: 120, width: 120
                    },
                ],
                rules: {
                    "username": webix.rules.isNotEmpty,
                    "password": webix.rules.isNotEmpty
                },
                width: 360, margin: 9,
            },
            {view: "label", minHeight: 6, height: 6},
            {
                view: "button", value: gettext("Forgot password"),
                name: "forgot_password_btn", id: "forgot_password_btn",
                href: "/password_reset/",
                click: function() {webix.send(this.config.href, {}, "GET");},
                minWidth: 165, width: 165,
                minHeight: 30, height: 30
            }
        ]
    }
});
var login_form = $$("login_form");


function postLoginForm() {
    var loginURL = window.location.href;
    if (login_form.validate()) {
        webix.ajax().post(
            loginURL,
            login_form.getValues(),
            function(text, data, xhr) {
                if (xhr["responseURL"] !== loginURL) {
                    webix.send(xhr["responseURL"], {}, "GET");
                } else {
                    webix.message({
                        text: gettext("Wrong username/password"),
                        type: "error",
                        expire: 3000,
                        id: "wrong_credentials_msg"
                    });
                }
            }
        )
    }
}

login_form.attachEvent("onSubmit", postLoginForm);
login_form.elements["login_btn"].attachEvent("onItemClick", postLoginForm);

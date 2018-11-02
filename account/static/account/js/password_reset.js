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

function multipleValidator() {
    var args = arguments;
    return function(value, row, name) {
        for (var i = 0; i < args.length; i++) {
            var obj = args[i], rule = obj.rule, message = obj.message;
            if (!rule.apply(this, arguments)) {
                this.elements[name].config.invalidMessage = message;
                return false;
            }
        }
        return true;
    }
}

webix.ui({ type: "space", rows: [{
    align: "center,middle",
    body: {
        rows: [
            {
                view: "template", type: "header",
                template: gettext("Password reset")
            },
            {
                view: "form", name: "password_reset_form",
                id: "password_reset_form", elements: [
                    {
                        view: "text", type: "text", value: csrfToken,
                        name: "csrfmiddlewaretoken", id: "csrfmiddlewaretoken",
                        hidden: true
                    },
                    {
                        view: "text", placeholder: gettext("E-mail"),
                        name: "email", id: "email"
                    },
                    {
                        view: "button", value: gettext("Reset"),
                        type: "form", name: "reset_btn", id: "reset_btn",
                        align: "center", minWidth: 120, width: 120
                    },
                ],
                rules: {
                    "email": multipleValidator(
                        {
                            rule: webix.rules.isNotEmpty,
                            message: gettext("E-mail can not be empty")
                        },
                        {
                            rule: webix.rules.isEmail,
                            message: gettext("Must be valid e-mail address")
                        }
                    )
                },
                width: 360, margin: 9,
            }
        ]
    }
}]});
var password_reset_form = $$("password_reset_form");


function postPasswordResetForm() {
    var passwordResetURL = "/profile/password_reset/";
    if (password_reset_form.validate()) {
        webix.ajax().post(
            passwordResetURL,
            password_reset_form.getValues(),
            function(text, data, xhr) {
                if (xhr["responseURL"] !== passwordResetURL) {
                    webix.send(xhr["responseURL"], {}, "GET");
                } else {
                    webix.message({
                        text: gettext("Could not send password reset confirmation"),
                        type: "error",
                        expire: 3000,
                        id: "error_sending_reset_confirm_msg"
                    });
                }
            }
        )
    }
}

password_reset_form.attachEvent("onSubmit", postPasswordResetForm);
password_reset_form.elements["reset_btn"].attachEvent(
    "onItemClick", postPasswordResetForm);

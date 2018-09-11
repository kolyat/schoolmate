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
                view: "template", type: "header",
                template: gettext("Enter new password"),
            },
            {
                view: "form", name: "new_password_form",
                id: "new_password_form", elements: [
                    {
                        view: "text", type: "text", value: csrfToken,
                        name: "csrfmiddlewaretoken", id: "csrfmiddlewaretoken",
                        hidden: true
                    },
                    {
                        view: "text", placeholder: gettext("New password"),
                        type: "password",
                        name: "new_password1", id: "new_password1",
                        invalidMessage: gettext("Field can not be empty")
                    },
                    {
                        view: "text",
                        placeholder: gettext("Retype new password"),
                        type: "password",
                        name: "new_password2", id: "new_password2",
                        invalidMessage: gettext("Field can not be empty")
                    },
                    {
                        view: "button", value: gettext("Confirm"),
                        type: "form", name: "confirm_btn", id: "confirm_btn",
                        align: "center", minWidth: 120, width: 120
                    },
                ],
                rules: {
                    "new_password1": webix.rules.isNotEmpty,
                    "new_password2": webix.rules.isNotEmpty,
                    $obj: function(data) {
                        if (data.new_password1 != data.new_password2) {
                            webix.message({
                                text: gettext("Passwords are not the same"),
                                type: "error",
                                expire: 1500,
                                id: "passwords_not_same_msg"
                            });
                            return false;
                        }
                        return true;
                    }
                },
                width: 360, margin: 9
            }
        ]
    }
});
var new_password_form = $$("new_password_form");


function postNewPasswordForm() {
    var newPasswordUrl = window.location.pathname;
    if (new_password_form.validate()) {
        webix.ajax().post(
            newPasswordUrl,
            login_form.getValues(),
            function(text, data, xhr) {
                if (xhr["responseURL"] !== newPasswordUrl) {
                    webix.send(xhr["responseURL"], {}, "GET");
                } else {
                    webix.message({
                        text: gettext("Could not set up new password"),
                        type: "error",
                        expire: 3000,
                        id: "error_setup_new_password_msg"
                    });
                }
            }
        )
    }
}

new_password_form.attachEvent("onSubmit", postNewPasswordForm);
new_password_form.elements["confirm_btn"].attachEvent(
    "onItemClick", postNewPasswordForm);

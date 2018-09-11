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

var personalInfoFormLabelWidth = 125;
personalInfoForm = {
    body: {
        rows: [
            {
                view: "template", template: gettext("User info"),
                type: "header", name: "user_info_header"
            },
            {
                view: "form",
                name: "personal_info_form", id: "personal_info_form",
                elements: [
                    {
                        view: "text", type: "text", value: csrfToken,
                        name: "csrfmiddlewaretoken", id: "csrfmiddlewaretoken",
                        hidden: true
                    },
                    {
                        view: "text", label: gettext("Username"),
                        name: "username", id: "username",
                        readonly: true, labelWidth: personalInfoFormLabelWidth
                    },
                    {
                        view: "text", label: gettext("First name"),
                        name: "first_name", id: "first_name",
                        readonly: true, labelWidth: personalInfoFormLabelWidth
                    },
                    {
                        view: "text", label: gettext("Patronymic name"),
                        name: "patronymic_name", id: "patronymic_name",
                        readonly: true, labelWidth: personalInfoFormLabelWidth
                    },
                    {
                        view: "text", label: gettext("Last name"),
                        name: "last_name", id: "last_name",
                        readonly: true, labelWidth: personalInfoFormLabelWidth
                    },
                    {
                        view: "text", label: gettext("Date of birth"),
                        name: "birth_date", id: "birth_date",
                        readonly: true, labelWidth: personalInfoFormLabelWidth,
                        format: webix.i18n.dateFormatStr
                    },
                    {
                        view: "text", label: gettext("E-mail"),
                        name: "email", id: "email",
                        readonly: true, labelWidth: personalInfoFormLabelWidth
                    },
                    {
                        view: "text", label: gettext("Form"),
                        name: "school_form", id: "school_form",
                        readonly: true, labelWidth: personalInfoFormLabelWidth
                    },
                    {
                        view: "select", label: gettext("Language"), value: "",
                        name: "language_select", id: "language_select",
                        labelWidth: personalInfoFormLabelWidth,
                        options: []
                    }
                ],
                type: "form", minWidth: 350, maxWidth: 420
            }
        ]
    }, align: "center"
};
passwordChangeForm = {
    body: {
        rows: [
            {
                view: "template", template: gettext("Change password"),
                type: "header", name: "change_password_header"
            },
            {
                view: "form",
                name: "password_change_form", id: "password_change_form",
                elements: [
                    {
                        view: "text", type: "text", value: csrfToken,
                        name: "csrfmiddlewaretoken", id: "csrfmiddlewaretoken",
                        hidden: true
                    },
                    {
                        view: "text", label: gettext("Current password"),
                        type: "password",
                        name: "old_password", id: "old_password",
                        invalidMessage: gettext("Field can not be empty"),
                        labelPosition: "top"
                    },
                    {
                        view: "text", label: gettext("New password"),
                        type: "password",
                        name: "new_password1", id: "new_password1",
                        invalidMessage: gettext("Field can not be empty"),
                        labelPosition: "top"
                    },
                    {
                        view: "text", label: gettext("Retype new password"),
                        type: "password",
                        name: "new_password2", id: "new_password2",
                        invalidMessage: gettext("Field can not be empty"),
                        labelPosition: "top"
                    },
                    {
                        view: "button", value: gettext("Change password"),
                        type: "form",
                        name: "change_password_btn", id: "change_password_btn",
                        align: "center", minWidth: 150, width: 150
                    },
                ],
                rules: {
                    "old_password": webix.rules.isNotEmpty,
                    "new_password1": webix.rules.isNotEmpty,
                    "new_password2": webix.rules.isNotEmpty,
                    $obj: function(data) {
                        if (data.new_password1 != data.new_password2) {
                            webix.message({
                                text: gettext("New passwords are not the same"),
                                type: "error",
                                expire: 3000,
                                id: "new_passwords_not_same_msg"
                            });
                            return false;
                        }
                        return true;
                    }
                },
                type: "form", minWidth: 250, maxWidth: 350
            }
        ]
    }, align: "center"
};
webix.ui({
    id: "account_layout", type: "space", paddingY: 30,
    rows: [
        {
            responsive: "account_layout", margin: 5,
            cols: [personalInfoForm, passwordChangeForm]
        }
    ]
});
var personal_info_form = $$("personal_info_form");
var password_change_form = $$("password_change_form");
var language_select = $$("language_select");


function loadPersonalInfoForm() {
    var response = webix.ajax().sync().get("/profile/user/info");
    var user_info = JSON.parse(response.responseText);
    if (!user_info) {
        webix.message({
            text: gettext("Failed to retrieve user info from server"),
            type: "error",
            expire: 3000,
            id: "failed_user_info_msg"
        });
        return false;
    }
    var languages = user_info.languages;
    for (var i = 0; i < languages.length; i++) {
        var language = languages[i];
        language_select.config["options"].push(
            {"id": language[0], "value": language[1]});
    }
    personal_info_form.parse(user_info, 'json');
    language_select.config["value"] = user_info.language;
    language_select.refresh();
    return true;
}

function patchLanguage(newv, oldv) {
    webix.ajax().headers(headers).patch(
        "/profile/user/info",
        { language: newv }, {
            success: function(text, data, xhr) {
                webix.message({
                    text: gettext("Language changed"),
                    type: "success",
                    expire: 3000,
                    id: "language_changed_msg"
                });
                document.location.reload(true);
            },
            error: function(text, data, xhr) {
                webix.message({
                    text: gettext("Language change failed"),
                    type: "error",
                    expire: 3000,
                    id: "language_change_failed_msg"
                });
                language_select.config["value"] = oldv;
                language_select.refresh();
            }
        }
    )
}

function postPasswordChangeForm() {
    if (password_change_form.validate()) {
        webix.ajax().post(
            "/password_change/",
            password_change_form.getValues(),
            function(text, data, xhr) {
                if (xhr["responseURL"].includes("/password_change/done/")) {
                    webix.message({
                        text: gettext("Password changed"),
                        type: "success",
                        expire: 3000,
                        id: "password_changed_msg"
                    });
                    password_change_form.clear();
                } else {
                    webix.message({
                        text: gettext("Password change failed"),
                        type: "error",
                        expire: 3000,
                        id: "password_change_failed_msg"
                    });
                }
            }
        )
    }
}

password_change_form.attachEvent("onSubmit", postPasswordChangeForm);
password_change_form.elements["change_password_btn"].attachEvent(
    "onItemClick", postPasswordChangeForm);
language_select.attachEvent("onChange", patchLanguage);
loadPersonalInfoForm()

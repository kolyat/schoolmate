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
var URL_USER_INFO = "/profile/user/info/";
var URL_PASSWD_CHANGE = "/profile/password_change/";
var URL_PASSWD_CHANGE_DONE = "/profile/password_change/done/";

//
// Widget description
//
var formMinWidth = 270;

var piFormLabelWidth = 120;
var personalInfoBlock = {
    align: "center", body: {
        view: "layout", id: "pi_layout", type: "space",
        borderless: true, rows: [
            {
                view: "form", type: "form", minWidth: formMinWidth,
                name: "personal_info_form", id: "personal_info_form",
                elements: [
                    {
                        view: "text", label: gettext("Username"),
                        name: "username", id: "username",
                        readonly: true, labelPosition: "top"
                    },
                    {
                        view: "text", label: gettext("First name"),
                        name: "first_name", id: "first_name",
                        readonly: true, labelPosition: "top"
                    },
                    {
                        view: "text", label: gettext("Patronymic name"),
                        name: "patronymic_name", id: "patronymic_name",
                        readonly: true, labelPosition: "top"
                    },
                    {
                        view: "text", label: gettext("Last name"),
                        name: "last_name", id: "last_name",
                        readonly: true, labelPosition: "top"
                    },
                    {
                        view: "text", label: gettext("Date of birth"),
                        name: "birth_date", id: "birth_date",
                        readonly: true, labelPosition: "top"
                        // format: webix.i18n.dateFormatStr
                    },
                    {
                        view: "text", label: gettext("E-mail"),
                        name: "email", id: "email",
                        readonly: true, labelPosition: "top"
                    },
                    {
                        view: "text", label: gettext("Form"),
                        name: "school_form", id: "school_form",
                        readonly: true, labelPosition: "top"
                    }
                ]
            }
        ]
    }
};

function patchUserInfo(newv, oldv, source) {
    var payload = {};
    payload[this.config.name] = newv;
    webix.ajax().headers(headers).patch(URL_USER_INFO, payload, {
        success: function(text, data, xhr) {
            webix.message({
                text: gettext("Settings changed"),
                type: "success",
                expire: messageExpireTime,
                id: "settings_changed_msg"
            });
            location.reload(true);
        },
        error: function(text, data, xhr) {
            webix.message({
                text: gettext("Settings change failed"),
                type: "error",
                expire: messageExpireTime,
                id: "settings_change_failed_msg"
            });
            this.config["value"] = oldv;
            this.refresh();
        }
    });
}
var settingsBlock = {
    align: "center", body: {
        view: "layout", id: "settings_layout", type: "space",
        borderless: true, rows: [
            {
                view: "form", type: "form", minWidth: formMinWidth,
                name: "settings_form", id: "settings_form",
                elements: [
                    {
                        view: "select", label: gettext("Language"), value: "",
                        name: "language", id: "language_select",
                        labelWidth: piFormLabelWidth, options: [], on: {
                            onChange: patchUserInfo
                        }
                    },
                    {
                        view: "select", label: gettext("Skin"), value: "",
                        name: "skin", id: "skin_select",
                        labelWidth: piFormLabelWidth, options: [], on: {
                            onChange: patchUserInfo
                        }
                    }
                ]
            },
            {
                view: "form", type: "form", minWidth: formMinWidth,
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
                        align: "center", minWidth: 150, maxWidth: 160
                    }
                ],
                rules: {
                    "old_password": webix.rules.isNotEmpty,
                    "new_password1": webix.rules.isNotEmpty,
                    "new_password2": webix.rules.isNotEmpty,
                    $obj: function(data) {
                        if (data.new_password1 !== data.new_password2) {
                            webix.message({
                                text: gettext("New passwords are not the same"),
                                type: "error",
                                expire: messageExpireTime,
                                id: "new_passwords_not_same_msg"
                            });
                            return false;
                        }
                        return true;
                    }
                }
            }
        ]
    }
};

var accountLayout = {
    view: "scrollview", id: "account_scroll", borderless: true, scroll: "y",
    body: {
        view: "flexlayout", id: "account_layout", type: "space",
        borderless: true, cols: [personalInfoBlock, settingsBlock]
    }
};

//
// UI init
//
webix.ui(accountLayout, main_layout, m_body);

var personal_info_form = $$("personal_info_form");

var language_select = $$("language_select");
var skin_select = $$("skin_select");

var password_change_form = $$("password_change_form");

//
// UI logic
//
function loadUserInfo() {
    var promise = webix.ajax().get(URL_USER_INFO);
    promise.then(data => {
        var user_info = data.json();
        personal_info_form.parse(user_info, "json");
        user_info.languages.forEach(language => {
            language_select.config["options"].push({
                "id": language["language_code"],
                "value": language["language_name"]
            });
        });
        language_select.config["value"] = user_info.language;
        language_select.refresh();
        user_info.skins.forEach(skin => {
            skin_select.config["options"].push({
                "id": skin["skin"],
                "value": skin["skin_name"]
            });
        });
        skin_select.config["value"] = user_info.skin;
        skin_select.refresh();
    }).fail(err => {
        webix.message({
            text: gettext("Failed to retrieve user info from server"),
            type: "error",
            expire: messageExpireTime,
            id: "failed_user_info_msg"
        });
    });
}

function postPasswordChangeForm() {
    if (password_change_form.validate()) {
        webix.ajax().post(URL_PASSWD_CHANGE, password_change_form.getValues(),
            function(text, data, xhr) {
                if (xhr["responseURL"].includes(URL_PASSWD_CHANGE_DONE)) {
                    webix.message({
                        text: gettext("Password changed"),
                        type: "success",
                        expire: messageExpireTime,
                        id: "password_changed_msg"
                    });
                    password_change_form.clear();
                } else {
                    webix.message({
                        text: gettext("Password change failed"),
                        type: "error",
                        expire: messageExpireTime,
                        id: "password_change_failed_msg"
                    });
                }
            }
        )
    }
}

//
// Event handling
//
password_change_form.attachEvent("onSubmit", postPasswordChangeForm);
password_change_form.elements["change_password_btn"].attachEvent(
    "onItemClick", postPasswordChangeForm);

//
// Start-up
//
loadUserInfo();

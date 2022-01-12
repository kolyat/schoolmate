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
var URL_MAIN = "/main/";

var URL_TIMETABLE = "/timetable/";
var URL_SCHOOL_FORMS = "/main/forms/";

var URL_DIARY = "/diary/";

var URL_NOTEBOOK = "/notebook/";

var URL_PROFILE = "/profile/";
var URL_GET_USERNAME = "/profile/user/";
var URL_LOGOUT = "/profile/logout/";

//
// Widget description
//
var toolbarHeight = 50;
var mainToolbar = {
    view: "toolbar", id: "main_toolbar", responsive: true, borderless: true,
    minHeight: toolbarHeight, height: toolbarHeight, cols: [
        {width: 1},
        {
            view: "icon", id: "app_menu_button", align: "center",
            icon: "mdi mdi-menu", responsiveCell: false
        },
        {id: "toolbar_block_left"},
        {id: "toolbar_block_right"},
        {
            view: "label", id: "app_label", label: "SCHOOLMATE",
            width: 150, align: "left", css: {
                "font-size": "18px",
                "letter-spacing": "2px"
            }
        }
    ]
};

var i_timetable_data = [
    {
        id: "f_0", value: gettext("All"), _url: URL_TIMETABLE,
        icon: "mdi mdi-file-table-box-multiple-outline", sf: 0
    }
];
var appMenu = {
    view: "sidebar", id: "app_menu", position: "left", responsiveCell: false,
    collapsed: true, collapsedWidth: 45, minWidth: 220, scroll: true,
    activeTitle: true, titleHeight: 45, multipleOpen: false, borderless: true,
    data: [
        {
            id: "i_main", value: gettext("Main"),
            icon: "mdi mdi-school", _url: URL_MAIN
        },
        {
            id: "i_timetable", value: gettext("Timetable"),
            icon: "mdi mdi-table", data: i_timetable_data
        },
        {
            id: "i_diary", value: gettext("Diary"),
            icon: "mdi mdi-book-open-variant", _url: URL_DIARY
        },
        {
            id: "i_notebook", value: gettext("Notebook"),
            icon: "mdi mdi-notebook-outline", _url: URL_NOTEBOOK
        },
        {
            id: "i_profile", value: gettext("Profile"),
            icon: "mdi mdi-account", data: [
                {
                    id: "i_profile_info", value: gettext("Info"),
                    icon: "mdi mdi-card-account-details-outline", _url: URL_PROFILE
                },
                //{
                //    id: "i_profile_settings", value: gettext("Settings"),
                //    icon: "mdi mdi-account-cog", _url: NONE
                //},
                {
                    id: "i_profile_logout", value: gettext("Log out"),
                    icon: "mdi mdi-exit-run", _url: URL_LOGOUT,
                }
            ]
        }
    ]
};

var mBody = {id: "m_body"};
var mainLayout = {
    view: "layout", type: "clean", responsive: true, borderless: true, rows: [
        {
            view: "layout", id: "main_layout", type: "clean",
            responsive: true, borderless: true, cols: [
                appMenu,
                mBody
            ]
        }
    ]
};

//
// UI init
//
webix.ui(mainToolbar, base_layout, b_header);
webix.ui(mainLayout, base_layout, b_body);

var main_layout = $$("main_layout");
var m_body = $$("m_body");

var main_toolbar = $$("main_toolbar");
var app_menu_button = $$("app_menu_button");
var app_menu = $$("app_menu");

//
// Event handling
//
function makeRequest(id) {
    var item = this.getItem(id);
    var payload = {};
    if (item.sf > -1) {
        payload["form_number"] = item.sf;
    }
    webix.send(item._url, payload, "GET");
}

function getForms() {
    var promise = webix.ajax().get(URL_SCHOOL_FORMS);
    promise.then(data => {
        var _forms = data.json();
        _forms.forEach(el => {
            var item = {
                id: "f_"+el["number"].toString(), value: el["number"].toString(),
                icon: "mdi mdi-file-table-box-outline", _url: URL_TIMETABLE,
                sf: el["number"]
            }
            i_timetable_data.push(item);
            app_menu.add(item, -1, "i_timetable");
        });
        var i_timetable = app_menu.getItem("i_timetable");
        i_timetable["menu"] = i_timetable_data;
        app_menu.updateItem("i_timetable", i_timetable);
    }).fail(err => {
        webix.message({
            text: gettext("Unable to get list of forms"),
            type: "error",
            expire: messageExpireTime,
            id: "unable_get_forms_msg"
        });
    });
}

app_menu.attachEvent("onAfterSelect", makeRequest);
app_menu_button.attachEvent("onItemClick", () => { app_menu.toggle(); });

//
// Start-up
//
webix.ajax().get(
    URL_GET_USERNAME,
    function(text, data, xhr) {
        var item = app_menu.getItem("i_profile");
        item["value"] = data.json().username;
        app_menu.updateItem("i_profile", item);
    }
);
getForms();

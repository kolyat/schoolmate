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
var URL_MAIN = "/main/";
var URL_TIMETABLE = "/timetable/";
var URL_DIARY = "/diary/";

var URL_GET_USERNAME = "/profile/user/";

var URL_PROFILE = "/profile/";
var URL_LOGOUT = "/profile/logout/";

//
// Widget description
//
var toolbarHeight = 50;

//
// UI init
//
webix.ui({
    view: "sidebar", id: "app_menu", position: "left", container: "div_menu",
    collapsed: true, collapsedWidth: 45, minWidth: 220, // maxWidth: 260
    activeTitle: true, titleHeight: 45, multipleOpen: false, borderless: true,
    data: [
        {
            id: "main", value: gettext("Main"),
            icon: "mdi mdi-school", href: URL_MAIN
        },
        {
            id: "timetable", value: gettext("Timetable"),
            icon: "mdi mdi-table", href: URL_TIMETABLE
        },
        {
            id: "diary", value: gettext("Diary"),
            icon: "mdi mdi-book-open-variant", href: URL_DIARY
        },
        {
            id: "profile", value: gettext("Profile"),
            icon: "mdi mdi-account", data: [
                {
                    id: "profile_info", value: gettext("Info"),
                    icon: "mdi mdi-card-account-details-outline", href: URL_PROFILE
                },
                // TODO: implement new views
                //{
                //    id: "profile_settings", value: gettext("Settings"),
                //    icon: "mdi mdi-account-cog", href: NONE
                //},
                {
                    id: "profile_logout", value: gettext("Log out"),
                    icon: "mdi mdi-exit-run", href: URL_LOGOUT,
                }
            ]
        }

    ]
});
var app_menu = $$("app_menu");

webix.ui({
    view: "toolbar", id: "main_toolbar", container: "div_header",
    responsive: true, minHeight: toolbarHeight, height: toolbarHeight,
    borderless: true, cols: [
        {width: 1},
        {
            view: "icon", id: "app_menu_button", align: "center",
            icon: "mdi mdi-menu"
        },
        {
            view: "label", id: "app_label", label: "SCHOOLMATE",
            width: 140, css: "headerSecondaryLabel", align: "right"
        },
        {id: "toolbar_block_left"},
        {id: "toolbar_block_right"},
        // TODO: display user's name
        {width: 1}
    ]
});

var main_toolbar = $$("main_toolbar");
var app_menu_button = $$("app_menu_button");
var app_label = $$("app_label");

//
// Event handling
//
function toggleAppMenu() {
    app_menu.toggle();
}

app_menu.attachEvent("onAfterSelect", function(id, e, node) {
    var item = this.getItem(id);
    webix.send(item.href, {}, "GET");
});
app_menu_button.attachEvent("onItemClick", toggleAppMenu);
app_label.attachEvent("onItemClick", toggleAppMenu);

//
// Start-up
//
// TODO: display user's name
//webix.ajax().get(
//    URL_GET_USERNAME,
//    function(text, data, xhr) {
//        var item = user_menu.getItem("user_item");
//        item["value"] = data.json().username;
//        user_menu.updateItem("user_item", item);
//    }
//);

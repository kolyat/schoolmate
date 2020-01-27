/*
Schoolmate - school management system
Copyright (C) 2018-2020  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>

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
var userMenu = {
    view: "menu", id: "user_menu", layout: "x", data: [
        {
            value: "", name: "user_item", id: "user_item", submenu: [
                {
                    value: gettext("Profile"),
                    name: "profile_item", id: "profile_item",
                    href: URL_PROFILE, config: {
                        click: function(id) {
                            webix.send(this.config.href, {}, "GET");
                        }
                    }
                },
                { $template: "Separator" },
                {
                    value: gettext("Log out"),
                    name: "logout_item", id: "logout_item",
                    href: URL_LOGOUT, config: {
                        click: function(id) {
                            webix.send(this.config.href, {}, "GET");
                        }
                    }
                }
            ]
        }
    ],
    submenuConfig: {css: "custom"},
    type: {subsign: true},
    autowidth: true, autoheight: true, minWidth: 90, maxWidth: 150,
    align: "right", css: {"text-align": "right", "padding": "9px 0px"}
};

//
// UI init
//
webix.ui({
    view: "toolbar", id: "main_toolbar",
    cols: [
        {
            view: "label", label: "SCHOOLMATE", align: "center",
            minWidth: 160, width: 180, css: "headerSecondaryLabel"
        },
        {},
        {
            view: "button", value: gettext("Main"), align: "left",
            name: "main_page_btn", id: "main_page_btn", href: URL_MAIN,
            click: function() {webix.send(this.config.href, {}, "GET");},
            minWidth: 90, width: 90, minHeight: 40, height: 40
        },
        {
            view: "button", value: gettext("Timetable"), align: "left",
            name: "timetable_btn", id: "timetable_btn", href: URL_TIMETABLE,
            click: function() {webix.send(this.config.href, {}, "GET");},
            minWidth: 90, width: 90, minHeight: 40, height: 40
        },
        {
            view: "button", value: gettext("Diary"), align: "left",
            name: "diary_btn", id: "diary_btn", href: URL_DIARY,
            click: function() {webix.send(this.config.href, {}, "GET");},
            minWidth: 90, width: 90, minHeight: 40, height: 40
        },
        {},
        userMenu
    ],
    minHeight: 60, height: 60
});

var user_menu = $$("user_menu");

//
// Start-up
//
webix.ajax().get(
    URL_GET_USERNAME,
    function(text, data, xhr) {
        var item = user_menu.getItem("user_item");
        item["value"] = data.json().username;
        user_menu.updateItem("user_item", item);
    }
);

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
var toolbarHeight = 60;

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
    view: "sidemenu", id: "app_menu", position: "left", hidden: true,
    width: 210, borderless: true,
    state: function(state) {
        state.top = toolbarHeight;
        state.height -= toolbarHeight;
    },
    body: {
        view: "list", id: "app_menu_list", borderless: true, scroll: false,
        template: "<span class='menu_item_icon #icon#'></span> #value#",
        type: {height: toolbarHeight, css: "app_menu_item"},
        data: [
            {id: 1, value: gettext("Main"), icon: "fas fa-school", href: URL_MAIN,},
            {id: 2, value: gettext("Timetable"), icon: "fas fa-table", href: URL_TIMETABLE},
            {id: 3, value: gettext("Diary"), icon: "fas fa-book-open", href: URL_DIARY},
        ]
    }
});
var app_menu = $$("app_menu");

webix.ui({
    view: "toolbar", id: "main_toolbar",
    minHeight: toolbarHeight, height: toolbarHeight,
    cols: [
        {
            view: "icon", icon: "fas fa-bars",
            minWidth: 50, width: 50, minHeight: 50, height: 50,
            click: function() {
                if (app_menu.config.hidden) {
                    app_menu.show();
                } else {
                    app_menu.hide();
                }
            }
        },
        {
            view: "label", label: "<a href='/'>SCHOOLMATE</a>", align: "center",
            minWidth: 160, width: 180, css: "headerSecondaryLabel"
        },
        {id: "toolbar_block_left"},
        {id: "toolbar_block_centre"},
        {id: "toolbar_block_right"},
        userMenu
    ]
});

var main_toolbar = $$("main_toolbar");
var user_menu = $$("user_menu");
var app_menu_list = $$("app_menu_list");

//
// Event handling
//
app_menu_list.attachEvent("onItemClick", function(id, e, node) {
    var item = this.getItem(id);
    webix.send(item.href, {}, "GET");
});

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

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

userMenu = {
    view: "menu", id: "user_menu", layout: "x", data: [
        {
            value: "", name: "user_item", id: "user_item", submenu: [
                {
                    value: gettext("Profile"),
                    name: "profile_item", id: "profile_item",
                    href: "/profile/", config: {
                        click: function(id) {
                            webix.send(this.config.href, {}, "GET");
                        }
                    }
                },
                { $template: "Separator" },
                {
                    value: gettext("Log out"),
                    name: "logout_item", id: "logout_item",
                    href: "/profile/logout/", config: {
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
webix.ui({
    view: "toolbar", id: "main_toolbar",
    cols: [
        {
            view: "label", label: "SCHOOLMATE", align: "center",
            minWidth: 150, width: 150,
        },
        {},
        {
            view: "button", value: gettext("Main"), align: "left",
            name: "main_page_btn", id: "main_page_btn", href: "/main",
            click: function() {webix.send(this.config.href, {}, "GET");},
            minWidth: 90, width: 90, minHeight: 40, height: 40
        },
        {},
        userMenu
    ],
    minHeight: 60, height: 60
});
var user_menu = $$("user_menu");


webix.ajax().get(
    "/profile/user",
    function(text, data, xhr) {
        var item = user_menu.getItem("user_item");
        item["value"] = data.json().username;
        user_menu.updateItem("user_item", item);
    }
);

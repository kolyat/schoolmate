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

webix.ui({ type: "space", rows: [{
    align: "center,middle",
    body: {
        rows: [
            {
                view: "form", name: "password_reset_sent_form",
                id: "password_reset_sent_form", elements: [
                    {
                        view: "label", label: gettext("Password reset confirmation has been sent to your e-mail"),
                        align: "center"
                    },
                    {
                        view: "button", value: gettext("Back to login page"),
                        name: "back_to_login_btn", id: "back_to_login_btn",
                        href: "/profile/login/",
                        click: function() {
                            webix.send(this.config.href, {}, "GET") },
                        align: "center", minWidth: 300, width: 300
                    },
                ],
                width: 660, margin: 9
            }
        ]
    }
}]});

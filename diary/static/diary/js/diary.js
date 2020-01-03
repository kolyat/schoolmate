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

var layoutMargin = 5;
var navBar = {
    view: "toolbar", id: "navbar", cols: [
        {},
        {
            view: "button", id: "prev_button", name: "prev_button",
            value: gettext("Previous"), label: "",
            type: "icon", css: "fas fa-angle-double-left",
            minWidth: 40, width: 50, minHeight: 30, height: 30, align: "right",
            click: function() {} // TODO: implement
        },
        {
            view: "datepicker", id: "current_date", stringResult: false,
            value: new Date(), icons: false, // TODO: define icon
            invalid: true, invalidMessage: gettext("Invalid date"),
            minWidth: 80, width: 120, minHeight: 30, height: 30, align: "center"
        },
        {
            view: "button", id: "next_button", name: "next_button",
            value: gettext("Next"), label: "",
            type: "icon", css: "fas fa-angle-double-right",
            minWidth: 40, width: 50, minHeight: 30, height: 30, align: "left",
            click: function() {} // TODO: implement
        },
        {}
    ],
    minHeight: 40, height: 40
};
webix.ui({
    type: "space", paddingY: 30,
    rows: [
        {
            id: "navbar_layout", margin: layoutMargin, cols: [navBar]
        },
        {
            id: "records_layout", margin: layoutMargin, cols: [
                {
                    id: "left_layout", responsive: "records_layout",
                    margin: layoutMargin, rows: [{}, {}, {}] // TODO: add tables
                },
                {
                    id: "right_layout", responsive: "records_layout",
                    margin: layoutMargin, rows: [{}, {}, {}] // TODO: add tables
                }
            ]
        },
        {gravity: 0.1}
    ]
});

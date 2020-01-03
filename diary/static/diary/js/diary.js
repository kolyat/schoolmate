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
            value: new Date(), icons: false,
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
var dayTableTemplate = {
    view: "datatable", autowidth: false, autoheight: true,
    fixedRowHeight: false, scrollX: false, rowHeight: 26, columns: [
        {
            id: "lesson_num", fillspace: 0.25, header: {
                text: "lesson_num", colspan: 2, height: 30,
                css: {"text-align": "center"}
            },
            // minWidth: 26, width: 28,
        },
        {
            id: "subject", header: "subject", fillspace: 1,
            // minWidth: 100, width: 140,
        },
        {
            id: "record", fillspace: 3.8, header: {
                text: "record", colspan: 3, css: {"text-align": "center"}
            },
            // minWidth: 140,
        },
        {
            id: "marks", header: "marks", fillspace: 0.5
            // minWidth: 50, width: 60,
        },
        {
            id: "signature", header: "signature", fillspace: 0.8
            // minWidth: 80, width: 100,
        }
    ],
    data: [ // TODO: remove test data
        {"id": 1, "lesson_num": 1, "subject": "Subject", "record": "Some records here", "marks": "3 5", "signature": "Signature"},
        {"id": 2, "lesson_num": 2, "subject": "Subject", "record": "Some records here", "marks": "3 5", "signature": "Signature"},
        {"id": 3, "lesson_num": 3, "subject": "Subject", "record": "Some records here", "marks": "3 5", "signature": "Signature"},
        {"id": 4, "lesson_num": 4, "subject": "Subject", "record": "Some records here; 0 1 2 3 4 5 6 7 8 9", "marks": "3 5 4", "signature": "Long signature"},
        {"id": 5, "lesson_num": 5, "subject": "Subject", "record": "Some records here", "marks": "3 5", "signature": "Signature"},
        {"id": 6, "lesson_num": 6, "subject": "Subject", "record": "Some records here", "marks": "3 5", "signature": "Signature"},
        {"id": 7, "lesson_num": 7, "subject": "Subject", "record": "Some records here", "marks": "3 5", "signature": "Signature"},
    ]
}
webix.ui({
    type: "line", paddingY: 2, rows: [
        {
            id: "navbar_layout", cols: [navBar]
        },
        {
            id: "records_layout", cols: [
                {
                    id: "left_layout", responsive: "records_layout",
                    type: "space", borderless: true, rows: [
                        dayTableTemplate,
                        dayTableTemplate,
                        dayTableTemplate
                    ] // TODO: add proper tables
                },
                {
                    id: "right_layout", responsive: "records_layout",
                    type: "space", borderless: true, rows: [
                        dayTableTemplate,
                        dayTableTemplate,
                        dayTableTemplate
                    ] // TODO: add proper tables
                }
            ]
        }
    ]
});

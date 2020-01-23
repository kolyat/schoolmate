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

var lessons_num = 7;
// For array comparison
var isequal = (a, b) => a.every((v, i) => v === b[i]);
                        // a.reduce((x, y) => x && b.includes(y), true);


var navBar = {
    view: "toolbar", id: "navbar", cols: [
        {},
        {
            view: "button", id: "prev_button", name: "prev_button",
            value: gettext("Previous"), tooltip: gettext("Previous"),
            type: "iconTop", css: "fas fa-angle-double-left",
            minWidth: 40, width: 50, minHeight: 30, height: 30, align: "right"
        },
        {
            view: "datepicker", id: "current_date", stringResult: false,
            value: new Date(), icons: false,
            invalid: true, invalidMessage: gettext("Invalid date"),
            minWidth: 80, width: 120, minHeight: 30, height: 30, align: "center"
        },
        {
            view: "button", id: "next_button", name: "next_button",
            value: gettext("Next"), tooltip: gettext("Next"),
            type: "icon", css: "fas fa-angle-double-right",
            minWidth: 40, width: 50, minHeight: 30, height: 30, align: "left"
        },
        {}
    ],
    minHeight: 40, height: 40
};

var dayTableTemplate = {
    view: "datatable", id: "", autowidth: false, autoheight: true,
    fixedRowHeight: false, scrollX: false, rowHeight: 26,
    editable: true, editaction: "dblclick", columns: [
        {
            id: "lesson_num", fillspace: 0.25, header: {
                text: "lesson_num", colspan: 2, height: 30,
                css: {"text-align": "center"}
            },
            // minWidth: 26, width: 28,
        },
        {
            id: "subject", header: "subject", fillspace: 1, editor: "select",
            options: [],
            // minWidth: 100, width: 140,
        },
        {
            id: "record", fillspace: 3.8, header: {
                text: "record", colspan: 3, css: {"text-align": "center"}
            }, editor: "popup",
            // minWidth: 140,
        },
        {
            id: "marks", header: "marks", fillspace: 0.55,
            // minWidth: 50, width: 60,
        },
        {
            id: "signature", header: "signature", fillspace: 0.8,
            // minWidth: 80, width: 100,
        }
    ],
    on: {
        onAfterEditStart: function(id) {
            var editor = this.getEditor(id);
            var popup = editor.getPopup();
            if (popup) {
                popup.config.width = this.getColumnConfig("record").width;
                popup.config.height = 120;
                popup.resize();
            }
        }
    },
    data: []
};
var dayTables = new Array();
var tablesNum = 6;
var daytable_id = "daytable";
for (var d = 0; d < tablesNum; d++) {
    dayTables.push(webix.copy(dayTableTemplate));
    dayTables[d].id = daytable_id + d;
    for (var l = 1; l < lessons_num+1; l++) {
        dayTables[d].data.push({
            "id": l,
            "lesson_num": l,
            "subject": "",
            "record": "",
            "marks": "",
            "signature": ""
        });
    }
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
                        dayTables[0],
                        dayTables[1],
                        dayTables[2],
                        {}
                    ]
                },
                {
                    id: "right_layout", responsive: "records_layout",
                    type: "space", borderless: true, rows: [
                        dayTables[3],
                        dayTables[4],
                        dayTables[5],
                        {}
                    ]
                }
            ]
        }
    ]
});

var current_date = $$("current_date");
var prev_button = $$("prev_button");
var next_button = $$("next_button");
var daytable = new Array();
for (var d = 0; d < tablesNum; d++) {
    daytable.push($$(daytable_id + d));
}


function getSubjects() {
    var promise = webix.ajax().get("/main/subjects/");
    promise.then(function(data) {
        var _subjects = new Array();
        data.json().forEach(element => _subjects.push(element.subject));
        for (var d = 0; d < tablesNum; d++) {
            var config = daytable[d].getColumnConfig("subject");
            config.collection.clearAll();
            config.collection.parse(_subjects);
        }
    }).fail(function(err) {
        webix.message({
            text: gettext("Failed to retrieve list of school subjects"),
            type: "error",
            expire: 3000,
            id: "failed_retrieve_subjects_msg"
        });
    });
}

var monday = 0;
function updateDates() {
    // Calculate dates of week
    var now = current_date.getValue();
    var delta = [0, 1, 2, 3, 4, 5, 6];
    delta = delta.map(val => val - now.getDay());
    var days_of_week = delta.map(val => {
        var _current_date = new Date(now);
        _current_date.setDate(_current_date.getDate() + val);
        return _current_date;
    });
    days_of_week.shift();
    var monday_now = days_of_week[0].getDate();
    // Set date for each table
    for (var d = 0; d < tablesNum; d++) {
        var _to_day_of_week = webix.Date.dateToStr("%l");
        var _to_month_day = webix.Date.dateToStr("%F, %j");
        daytable[d].getColumnConfig("lesson_num").header[0]
        .text = _to_day_of_week(days_of_week[d]);
        daytable[d].getColumnConfig("record").header[0]
        .text = _to_month_day(days_of_week[d]);
        daytable[d].refreshColumns();
        if (monday_now !== monday) {
            var _d = days_of_week[d].getDate();
            var _m = days_of_week[d].getMonth()+1;
            var _y = days_of_week[d].getFullYear();
            daytable[d].load(`/diary/${_y}/${_m}/${_d}/`).then().fail(err => {
                webix.message({
                    text: gettext("Failed to get records dated ") +
                        `${_y}.${_m}.${_d}/`,
                    type: "error",
                    expire: 3000,
                    id: "failed_get_records_msg"
                });
            });
        }
    }
    monday = monday_now;
}


prev_button.attachEvent("onItemClick", function() {
    var _date = current_date.getValue();
    _date.setDate(_date.getDate() - 7);
    current_date.setValue(_date);
});
next_button.attachEvent("onItemClick", function() {
    var _date = current_date.getValue();
    _date.setDate(_date.getDate() + 7);
    current_date.setValue(_date);
});
getSubjects();
updateDates();
current_date.attachEvent("onChange", updateDates);

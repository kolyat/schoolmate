/*
Schoolmate - school management system
Copyright (C) 2018-2023  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>

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
var lessons_num = 7;
// Function for array comparison
var isequal = (a, b) => a.every((v, i) => v === b[i]);
                        // a.reduce((x, y) => x && b.includes(y), true);

var URL_SUBJECTS = "/main/subjects/";

//
// Widget description
//
var navBar = {
    view: "layout", type: "clean", id: "navbar", paddingY: 8,
    responsive: false, borderless: true, cols: [
        {
            view: "icon", id: "prev_button", align: "center",
            icon: "mdi mdi-chevron-left-box-outline", css: "weekChangeButton",
            tooltip: gettext("Previous week")
        },
        {
            view: "datepicker", id: "current_date", stringResult: false,
            value: new Date(), icons: false, minWidth: 100, width: 120,
            invalid: true, invalidMessage: gettext("Invalid date")
        },
        {
            view: "icon", id: "next_button", align: "center",
            icon: "mdi mdi-chevron-right-box-outline", css: "weekChangeButton",
            tooltip: gettext("Next week")
        }
    ]
};

var tablesNum = 6;
var daytable_id = "daytable";
var dayTableTemplate = {
    view: "datatable", id: "", autowidth: false, autoheight: true,
    fixedRowHeight: false, scrollX: false, rowHeight: 26, date: new Date(),
    editable: true, tooltip: true, editaction: "dblclick", columns: [
        {
            id: "lesson_number", fillspace: 0.25, header: {
                text: "lesson_number", colspan: 2, height: 30,
                css: {"text-align": "center"}
            }
        },
        {
            id: "subject", header: "subject", fillspace: 1.2, editor: "select",
            options: []
        },
        {
            id: "text", fillspace: 3.8, header: {
                text: "text", colspan: 3, css: {"text-align": "center"}
            }, editor: "popup"
        },
        {
            id: "marks", header: "marks", maxWidth: 1
        },
        {
            id: "signature", header: "signature", maxWidth: 1
        }
    ],
    on: {
        onAfterEditStart: function(id) {
            var editor = this.getEditor(id);
            var popup = null;
            try {
                var popup = editor.getPopup();
            } catch(err) {}
            if (popup) {
                popup.config.width = this.getColumnConfig("text").width;
                popup.config.height = 120;
                popup.resize();
            }
        },
        onAfterEditStop: function(state, editor, ignoreUpdate) {
            if ((state.value == state.old) || ignoreUpdate) return false;
            var _d = this.config.date.getDate();
            var _m = this.config.date.getMonth()+1;
            var _y = this.config.date.getFullYear();
            var _record = this.getItem(editor.row);
            webix.ajax().headers(headers).post(`/diary/${_y}/${_m}/${_d}/`, {
                "lesson_number": editor.row,
                "subject": _record.subject,
                "text": _record.text
            }).then(() => {
                webix.message({
                    text: gettext("Record saved"),
                    type: "success",
                    expire: messageExpireTime,
                    id: "saved_record_msg"
                });
                return true;
            }).fail(err => {
                webix.message({
                    text: gettext("Failed to save record to ") +
                        `${_d}.${_m}.${_y}`,
                    type: "error",
                    expire: messageExpireTime,
                    id: "failed_save_record_msg"
                });
                return false;
            });
        }
    },
    data: []
};

var dayTables = new Array();
for (var d = 0; d < tablesNum; d++) {
    dayTables.push(webix.copy(dayTableTemplate));
    dayTables[d].id = daytable_id + d;
    for (var l = 1; l < lessons_num+1; l++) {
        dayTables[d].data.push({
            "id": l,
            "lesson_number": l,
            "subject": " ",
            "text": "",
            "marks": "",
            "signature": ""
        });
    }
}

var diaryLayout = {
    view: "scrollview", id: "diary_scroll", borderless: true, scroll: "y",
    body: {
        view: "flexlayout", id: "diary_layout", type: "clean",
        borderless: true, cols: [
            {
                view: "layout", id: "left_layout", type: "space",
                borderless: true, minWidth: 300, rows: [
                    dayTables[0],
                    dayTables[1],
                    dayTables[2]
                ]
            },
            {
                view: "layout", id: "right_layout", type: "space",
                borderless: true, minWidth: 300, rows: [
                    dayTables[3],
                    dayTables[4],
                    dayTables[5]
                ]
            }
        ]
    }
};

//
// UI init
//
var pos = main_toolbar.index($$("toolbar_block_right"));
main_toolbar.addView(navBar, pos);

webix.ui(diaryLayout, main_layout, m_body);

var diary_layout = $$("diary_layout");

var current_date = $$("current_date");
var prev_button = $$("prev_button");
var next_button = $$("next_button");

var daytable = new Array();
for (var d = 0; d < tablesNum; d++) {
    daytable.push($$(daytable_id + d));
}

//
// UI logic
//
function getSubjects() {
    var promise = webix.ajax().get(URL_SUBJECTS);
    promise.then(data => {
        var _subjects = new Array();
        data.json().forEach(element => _subjects.push(element.subject));
        for (var d = 0; d < tablesNum; d++) {
            var config = daytable[d].getColumnConfig("subject");
            config.collection.clearAll();
            config.collection.parse(_subjects);
        }
    }).fail(err => {
        webix.message({
            text: gettext("Failed to retrieve list of school subjects"),
            type: "error",
            expire: messageExpireTime,
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
        daytable[d].config.date.setDate(days_of_week[d].getDate());
        daytable[d].getColumnConfig("lesson_number").header[0]
        .text = _to_day_of_week(days_of_week[d]);
        daytable[d].getColumnConfig("text").header[0]
        .text = _to_month_day(days_of_week[d]);
        daytable[d].refreshColumns();
        if (monday_now !== monday) {
            var _d = days_of_week[d].getDate();
            var _m = days_of_week[d].getMonth()+1;
            var _y = days_of_week[d].getFullYear();
            daytable[d].clearAll();
            daytable[d].load(`/diary/${_y}/${_m}/${_d}/`).then().fail(err => {
                webix.message({
                    text: gettext("Failed to get records dated ") +
                        `${_y}.${_m}.${_d}`,
                    type: "error",
                    expire: messageExpireTime,
                    id: "failed_get_records_msg"
                });
            });
        }
    }
    monday = monday_now;
}

function changeCurrentDate(direction) {
    var _date = current_date.getValue();
    _date.setDate(_date.getDate() + 7 * direction);
    current_date.setValue(_date);
    current_date.refresh();
    updateDates();
}

//
// Event handling
//
prev_button.attachEvent("onItemClick", () => {changeCurrentDate(-1)});
next_button.attachEvent("onItemClick", () => {changeCurrentDate(+1)});
diary_layout.attachEvent("onSwipeX", function(start, end) {
    if (end.x - start.x > 0) {
        // swipe from left to right
        changeCurrentDate(-1);
    } else {
        // swipe from right to left
        changeCurrentDate(+1);
    }
});

//
// Start-up
//
getSubjects();
updateDates();
current_date.attachEvent("onChange", updateDates);
$$("diary_layout").adjust();

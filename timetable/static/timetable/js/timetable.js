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
var URL_SCHOOL_FORMS = "/main/forms/";
var URL_TIMETABLE_DATA = "/timetable/data/";

//
// Widget description and init
//
var formTree = {view: "tree", id: "form_tree", width: 125};
var timeTable = {
    view: "datatable", id: "timetable", fixedRowHeight: false,
    leftSplit: 1, columns: [
        {id: "root", header: "", fillspace: true}
    ]
};

webix.ui({
    id: "timetable_layout", type: "space", container: "div_main", padding: 0,
    rows: [
        {
            cols: [
                formTree, {view: "resizer"}, timeTable
            ]
        }
    ]
});

var form_tree = $$("form_tree");
var timetable = $$("timetable");

//
// UI logic
//
var DAYS_OF_WEEK = new Map([
    [2, gettext("Monday")],
    [3, gettext("Tuesday")],
    [4, gettext("Wednesday")],
    [5, gettext("Thursday")],
    [6, gettext("Friday")],
    [7, gettext("Saturday")]
]);
var lessons_num = 7;
var school_forms = new Map();

function getTimetable(number) {
    timetable.clearAll(false);
    timetable.config.columns.splice(1, timetable.config.columns.length - 1);
    timetable.config.columns[0].fillspace = true;
    timetable.refreshColumns();
    timetable.refresh();
    timetable.hideOverlay();
    timetable.showOverlay(gettext("Loading..."));
    var params = 0;
    if (number > 0) params = number;
    var promise = webix.ajax().get(URL_TIMETABLE_DATA + params);
    var rows = new Object();
    DAYS_OF_WEEK.forEach((_, d) => {
        var lessons = new Array();
        for (var i = 0; i < lessons_num; i++) {
            var lesson = {root: i + 1};
            lessons.push(lesson);
        }
        rows[d] = lessons;
    });
    promise.then(data => {
        var tt = data.json();
        timetable.config.columns[0].fillspace = false;
        tt.forEach(form => {
            var f = [form.form_number.toString(), form.form_letter].join("");
            var f_subj = ["subj", f].join("_")
            var f_room = ["room", f].join("_")
            timetable.config.columns.push({
                id: f_subj, header: {
                    text: f, colspan: 2, css: {
                        "text-align": "center",
                        "font-weight": "bold"
                    }
                }
            });
            timetable.config.columns.push({id: f_room, header: "", width: 45});
            DAYS_OF_WEEK.forEach((_, d) => {
                var _lessons = form.lessons.filter(l => l.day_of_week === d);
                if (!_lessons) return;
                for (var i = 0; i < lessons_num; i++) {
                    var _subjects = _lessons.filter(
                        s => s.lesson_number === i + 1);
                    if (!_subjects) return;
                    var _subjs = new Array();
                    var _rooms = new Array();
                    _subjects.forEach(s => {
                        _subjs.push(s.subject);
                        var _room = s.classroom;
                        if (_room) {
                            _rooms.push(_room);
                        } else {
                            _rooms.push(" ");
                        }
                    });
                    rows[d][i][f_subj] = _subjs.join("<br>");
                    rows[d][i][f_room] = _rooms.join("<br>");
                }
            });
        });
        timetable.config.columns.push(
            {id: "extra", header: "", fillspace: true});
        timetable.config.columns[0].width = 110;
        timetable.refreshColumns();
        DAYS_OF_WEEK.forEach((day_name, day_number) => {
            timetable.add(
                {root: day_name, $css: "webix_ss_header"});
            rows[day_number].forEach(lesson => timetable.add(lesson));
        });
        var max_width = 0;
        timetable.eachColumn(id => {
            if (id.includes("subj")) {
                timetable.adjustColumn(id);
                var _width = timetable.getColumnConfig(id).width;
                if (_width > max_width) {
                    max_width = _width;
                }
            }
        });
        timetable.eachColumn(id => {
            if (id.includes("subj")) {
                timetable.setColumnWidth(id, max_width);
            }
        });
        timetable.adjustRowHeight();
        timetable.refresh();
        timetable.hideOverlay();
    }).fail(err => {
        timetable.hideOverlay();
        timetable.showOverlay(gettext("No data"));
        webix.message({
            text: gettext("Unable to retrieve timetable"),
            type: "error",
            expire: messageExpireTime,
            id: "unable_get_timetable_msg"
        });
    });
}

function getForms() {
    var promise = webix.ajax().get(URL_SCHOOL_FORMS);
    promise.then(data => {
        var _forms = data.json();
        form_tree.add({id: "form_numbers", value: gettext("Forms")});
        form_tree.add({id: "0", value: gettext("All")}, -1, "form_numbers");
        _forms.forEach(el => {
            school_forms.set(el["number"], el["letters"]);
            form_tree.add(
                {id: el["number"].toString(), value: el["number"].toString()},
                -1, "form_numbers"
            );
        });
        form_tree.open("form_numbers");
    }).fail(err => {
        webix.message({
            text: gettext("Unable to get list of forms"),
            type: "error",
            expire: messageExpireTime,
            id: "unable_get_forms_msg"
        });
    });
}

//
// Start-up
//
getForms();
form_tree.attachEvent("onItemClick", function(id) {
    var _number = parseInt(id);
    if (Number.isInteger(_number)) {
        getTimetable(_number);
    }
});
timetable.showOverlay(gettext("Select form to load timetable"));

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

var formTree = {view: "tree", id: "form_tree", width: 125};
var timeTable = {
    view: "datatable", id: "timetable", columns: [
        {id: "root", header: "", fillspace: true}
    ]
};
webix.ui({
    id: "timetable_layout", type: "space", padding: 0,
    rows: [{cols: [formTree, {view: "resizer"}, timeTable]}]
});
var form_tree = $$("form_tree");
var timetable = $$("timetable");


var DAYS_OF_WEEK = {
    2: gettext("Monday"),
    3: gettext("Tuesday"),
    4: gettext("Wednesday"),
    5: gettext("Thursday"),
    6: gettext("Friday"),
    7: gettext("Saturday")
};
var school_forms = new Map();

function getTimetable(number) {
    if (number > 0) {
        params = {form_number: number};
    } else {
        params = {};
    }
    timetable.config.columns.splice(1, timetable.config.columns.length - 1);
    timetable.config.columns[0].fillspace = true;
    timetable.refreshColumns();
    timetable.refresh();
    timetable.hideOverlay();
    timetable.showOverlay(gettext("Loading..."));
    var promise = webix.ajax().get("/timetable/data/", params);
    promise.then(function(data) {
        var tt = data.json();
        timetable.config.columns[0].fillspace = false;
        timetable.config.columns[0].width = 90;
        tt.forEach(function(form) {
            var f = [form.form_number.toString(), form.form_letter].join("");
            timetable.config.columns.push({id: f, header: f});
        });
        timetable.refreshColumns();
        timetable.refresh();
        timetable.hideOverlay();
    }).fail(function(err) {
        timetable.hideOverlay();
        timetable.showOverlay(gettext("No data"));
        webix.message({
            text: gettext("Unable to retrieve timetable"),
            type: "error",
            expire: 3000,
            id: "unable_get_timetable_msg"
        });
    });
}

function getForms() {
    var promise = webix.ajax().get("/main/forms/");
    promise.then(function(data) {
        var _forms = data.json();
        form_tree.add({id: "form_numbers", value: gettext("Forms")});
        form_tree.add({id: "0", value: gettext("All")}, -1, "form_numbers");
        _forms.forEach(function(el) {
            school_forms.set(el["number"], el["letters"]);
            form_tree.add(
                {id: el["number"].toString(), value: el["number"].toString()},
                -1, "form_numbers"
            );
        });
        form_tree.open("form_numbers");
    }).fail(function(err) {
        webix.message({
            text: gettext("Unable to get list of forms"),
            type: "error",
            expire: 3000,
            id: "unable_get_forms_msg"
        });
    });
}

getForms();
form_tree.attachEvent("onItemClick", function(id) {
    var _number = parseInt(id);
    if (Number.isInteger(_number)) {
        getTimetable(_number);
    }
});
timetable.showOverlay(gettext("Select form to load timetable"));

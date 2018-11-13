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
var subjectTable = {view: "datatable", id: "subject_table"};
webix.ui({
    id: "timetable_layout", type: "space", padding: 0,
    rows: [{cols: [
        formTree,
        {view: "resizer"},
        subjectTable,
    ]}]
});
var form_tree = $$("form_tree");
var subject_table = $$("subject_table");


var school_forms;

function getForms() {
    var promise = webix.ajax().get("/main/forms/");
    promise.then(function(data) {
        school_forms = data.json();
        form_tree.add({id: "form_numbers", value: gettext("Forms")});
        form_tree.add({id: "all", value: gettext("All")}, -1, "form_numbers");
        school_forms.forEach(function(el) {
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

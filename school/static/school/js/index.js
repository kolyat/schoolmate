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

var formWidth = 360;
var timeForm = {
    body: {
        rows: [
            {
                view: "form", name: "time_form", id: "time_form", elements: [
                    {
                        view: "label", id: "time_label", align: "center",
                        css: {"font-size": "36px"},
                        format: webix.i18n.timeFormat
                    }
                ], width: formWidth
            }
        ]
    }, align: "center"
};
var dateForm = {
    body: {
        rows: [
            {
                view: "form", name: "date_form", id: "date_form", elements: [
                    {
                        view: "calendar", id: "main_calendar",
                        events: webix.Date.isHoliday, weekHeader: true
                    }
                ], width: formWidth
            }
        ]
    }, align: "center"
};
webix.ui({
    id: "index_layout", type: "space", paddingY: 30,
    rows: [
        {responsive: "index_layout", margin: 5, cols: [timeForm]},
        {responsive: "index_layout", margin: 5, cols: [dateForm]},
    ]
});
var time_form = $$("time_form");
var time_label = $$("time_label");
var date_form = $$("date_form");
var main_calendar = $$("main_calendar");


var now = new Date();

function updateStatus() {
    var response = webix.ajax().sync().get("/main/status/");
    var status = JSON.parse(response.responseText);
    if (status) {
        now.setFullYear(status["year"], status["month"] - 1, status["day"]);
        now.setHours(status["hour"], status["minute"], status["second"]);
    } else {
        webix.message({
            text: gettext("Failed to retrieve date/time info from server"),
            type: "error",
            expire: 3000,
            id: "failed_status_info_msg"
        });
    }
    return status;
}

function updateTime(status) {
    time_label.setValue(webix.i18n.timeFormatStr(now));
    var views = time_form.getChildViews();
    for (var i = 0; i < views.length; i++) {
        if (views[i].config["id"] !== "time_label") {
            time_form.removeView(views[i].config["id"]);
        }
    }
    if (status["time_description"]) {
        var time_description = status["time_description"];
        for (var i = 0; i < time_description.length; i++) {
            time_form.addView({
                view: "label", align: "center",
                label: time_description[i]["description"]
            });
        }
    }
    time_form.refresh();
}

function updateDate(status) {
    main_calendar.setValue(now);
    var views = date_form.getChildViews();
    for (var i = 0; i < views.length; i++) {
        if (views[i].config["id"] !== "main_calendar") {
            date_form.removeView(views[i].config["id"]);
        }
    }
    if (status["date_description"]) {
        var date_description = status["date_description"];
        for (var i = 0; i < date_description.length; i++) {
            date_form.addView({
                view: "label", align: "center",
                label: date_description[i]["description"]
            });
        }
    }
    date_form.refresh();
}

time_label.setValue(webix.i18n.timeFormatStr(now));
var s = updateStatus();
updateTime(s);
updateDate(s);
window.setInterval(function() {
    var prev_minute = now.getMinutes();
    var prev_day = now.getDay();
    now.setSeconds(now.getSeconds() + 1);
    if (now.getMinutes() !== prev_minute) {
        s = updateStatus();
        updateTime(s);
        if (now.getDay() !== prev_day) {
            updateDate(s);
        }
    }
}, 1000);

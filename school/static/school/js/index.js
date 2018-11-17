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

var statusFormWidth = 300;
var statusLayoutMargin = 5;
var statusLayoutMaxWidth;
statusLayoutMaxWidth = statusFormWidth + statusLayoutMargin * 2;
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
                ], width: statusFormWidth
            }
        ]
    }, align: "left"
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
                ], width: statusFormWidth
            }
        ]
    }, align: "left"
};
var infoTab = {
    id: "info_tab", view: "tabview", responsive: "index_layout", cells: [
        {header: "News", body: {}},
        {header: "Schedules", body: {}}
    ]
};
webix.ui({
    type: "space", paddingY: 30,
    rows: [
        {
            id: "index_layout", cols: [
                {
                    id: "status_layout", responsive: "index_layout",
                    maxWidth: statusLayoutMaxWidth, margin: statusLayoutMargin,
                    rows: [timeForm, dateForm]
                },
                infoTab
            ]
        },
    ]
});
var time_form = $$("time_form");
var time_label = $$("time_label");
var date_form = $$("date_form");
var main_calendar = $$("main_calendar");


var now = new Date();

function updateClock(t) {
    time_label.setValue(webix.i18n.timeFormatStr(t));
}
function updateTimeStatus(_status) {
    time_form.getChildViews().filter(
        function(e) { return e.config["id"] !== "time_label"; }).forEach(
        function(e) { time_form.removeView(e.config["id"]); });
    if (_status["time_description"]) {
        _status["time_description"].forEach(function(el) {
            time_form.addView({view: "label", align: "center",
                               label: el["description"]});
        });
    }
    time_form.refresh();
}

function updateCalendar(d) {
    main_calendar.setValue(d);
}
function updateDateStatus(_status) {
    date_form.getChildViews().filter(
        function(e) { return e.config["id"] !== "main_calendar"; }).forEach(
        function(e) { date_form.removeView(e.config["id"]); });
    if (_status["date_description"]) {
        _status["date_description"].forEach(function(el) {
            date_form.addView({view: "label", align: "center",
                               label: el["description"]});
        });
    }
    date_form.refresh();
}

function updateStatus() {
    var promise = webix.ajax().get("/main/status/");
    promise.then(function(data) {
        var _status = data.json();
        now.setFullYear(_status["year"], _status["month"] - 1, _status["day"]);
        now.setHours(_status["hour"], _status["minute"], _status["second"]);
        updateClock(now);
        updateTimeStatus(_status);
        updateCalendar(now);
        updateDateStatus(_status);
    }).fail(function(err) {
        webix.message({
            text: gettext("Failed to retrieve date/time info from server"),
            type: "error",
            expire: 3000,
            id: "failed_status_info_msg"
        });
        updateTimeStatus({});
        updateDateStatus({});
    });
}

updateClock(now);
updateStatus();
window.setInterval(function() {
    var prev_minute = now.getMinutes();
    var prev_day = now.getDay();
    now.setSeconds(now.getSeconds() + 1);
    if (now.getMinutes() !== prev_minute) {
        updateStatus();
        updateClock(now);
        if (now.getDay() !== prev_day) {
            updateCalendar(now);
        }
    }
}, 1000);

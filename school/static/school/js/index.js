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
var URL_STATUS = "/main/status/";

var URL_YEAR_SCHEDULE = "/main/schedule/year/";
var URL_DAY_SCHEDULE = "/main/schedule/day/";

var URL_NEWS = "/news/";

//
// Widget description
//
var statusFormWidth = 300;

var timeBlock = {
    view: "form", name: "time_form", id: "time_form",
    width: statusFormWidth, elements: [
        {
            view: "label", id: "time_label", align: "center",
            css: "timeLabel", format: webix.i18n.timeFormat
        }
    ]
};

var dateBlock = {
    view: "form", name: "date_form", id: "date_form",
    width: statusFormWidth, elements: [
        {
            view: "calendar", id: "main_calendar",
            events: webix.Date.isHoliday, weekHeader: true
        }
    ]
};

var newsPager = {
    view: "pager", id: "news_pager", size: 10, group: 5,
    template: "{common.first()}{common.prev()}{common.pages()}"+
              "{common.next()}{common.last()}"
};
var newsView = {
    view: "list", id: "news_view", url: URL_NEWS, datatype: "json",
    datafetch: 10, datathrottle: 1000, loadahead: 30,
    template: function(obj) {
        var _created = webix.i18n.dateFormatStr(
            webix.i18n.parseFormatDate(obj.created));
        var _title = obj.title ? obj.title : "";
        var _content = obj.content;
        var _author = obj.author ? obj.author : "<br>";
        return "<div style='display:block;margin-top:6px;margin-bottom:6px;'>"+
               "<p style='text-align:right;'>"+_created+"</p>"+
               "<p style='text-align:left;font-weight:bold;'>"+_title+"</p>"+
               "<p style='text-align:left;'>"+_content+"</p>"+
               "<p style='text-align:right;font-style:italic;'>"+_author+"</p>"+
               "</div>";
    },
    pager: "news_pager", type: {height: "auto"}, scroll: "y",
    ready: function() {
        this.hideOverlay();
        if (!this.count()) {
            this.showOverlay(gettext("No data"));
        }
    }
};

var yearScheduleList = {
    view: "list", id: "year_schedule_list",
    url: URL_YEAR_SCHEDULE, datatype: "json",
    template: function(obj) {
        return "<div style='float:left;'>"+obj.description+"</div>"+
               "<div style='float:right;'>"+
               webix.i18n.dateFormatStr(webix.i18n.parseFormatDate(obj.start_date))+
               " – "+
               webix.i18n.dateFormatStr(webix.i18n.parseFormatDate(obj.end_date))+
               "</div>";
    },
    ready: function() {
        this.hideOverlay();
        if (!this.count()) {
            this.showOverlay(gettext("No data"));
            webix.message({
                text: gettext("Failed to get year schedule"),
                type: "error",
                expire: messageExpireTime,
                id: "filed_get_year_schedule_msg"
            });
        }
    }
};
var dailyScheduleList = {
    view: "list", id: "daily_schedule_list",
    url: URL_DAY_SCHEDULE, datatype: "json",
    template: function(obj) {
        return "<div style='float:left;'>"+obj.description+"</div>"+
               "<div style='float:right;'>"+
               webix.i18n.timeFormatStr(webix.i18n.parseTimeFormatDate(obj.start_time))+
               " – "+
               webix.i18n.timeFormatStr(webix.i18n.parseTimeFormatDate(obj.end_time))+
               "</div>";
    },
    ready: function() {
        this.hideOverlay();
        if (!this.count()) {
            this.showOverlay(gettext("No data"));
            webix.message({
                text: gettext("Failed to get daily schedule"),
                type: "error",
                expire: messageExpireTime,
                id: "filed_get_daily_schedule_msg"
            });
        }
    }
};

var infoBlock = {
    id: "info_tab", view: "tabview", responsive: true,
    type: "space", borderless: false, margin: 0, minWidth: statusFormWidth,
    cells: [
        {
            header: gettext("News"), rows: [newsView, newsPager]
        },
        {
            header: gettext("Schedules"), rows: [
                {
                    view: "template", template: gettext("Year schedule"),
                    type: "header"
                },
                yearScheduleList,
                {
                    view: "template", template: gettext("Daily schedule"),
                    type: "header"
                },
                dailyScheduleList
            ]
        }
    ]
};

var indexLayout = {
    view: "layout", id: "index_layout", type: "clean",
    responsive: true, borderless: true, cols: [
        {
            view: "layout", type: "space", responsive: true,
            borderless: true, rows: [
                timeBlock,
                dateBlock,
                {}
            ]
        },
        infoBlock
    ]
}

//
// UI init
//
webix.ui(indexLayout, main_layout, m_body);

var time_form = $$("time_form");
var time_label = $$("time_label");

var date_form = $$("date_form");
var main_calendar = $$("main_calendar");

var news_view = $$("news_view");

var year_schedule_list = $$("year_schedule_list");
var daily_schedule_list = $$("daily_schedule_list");

webix.extend(news_view, webix.OverlayBox);
news_view.attachEvent("onBeforeLoad", function() {
    news_view.showOverlay(gettext("Loading..."));
});
news_view.attachEvent("onLoadError", function() {
    webix.message({
        text: gettext("Failed to load news"),
        type: "error",
        expire: messageExpireTime,
        id: "failed_load_news_msg"
    });
});

webix.extend(year_schedule_list, webix.OverlayBox);
year_schedule_list.attachEvent("onBeforeLoad", function() {
    year_schedule_list.showOverlay(gettext("Loading..."));
});

webix.extend(daily_schedule_list, webix.OverlayBox);
daily_schedule_list.attachEvent("onBeforeLoad", function() {
    daily_schedule_list.showOverlay(gettext("Loading..."));
});

//
// UI logic
//
var now = new Date();

function updateClock(t) {
    time_label.setValue(webix.i18n.timeFormatStr(t));
}

function updateTimeStatus(_status) {
    time_form.getChildViews().filter(
        function(e) { return e.config["id"] !== "time_label"; }
    ).forEach(
        function(e) { time_form.removeView(e.config["id"]); }
    );
    if (_status["time_description"]) {
        _status["time_description"].forEach(el => {
            time_form.addView({
                view: "label",
                align: "center",
                label: el["description"]
            });
        });
    }
    time_form.refresh();
}

function updateCalendar(d) {
    main_calendar.setValue(d);
}

function updateDateStatus(_status) {
    date_form.getChildViews().filter(
        function(e) { return e.config["id"] !== "main_calendar"; }
    ).forEach(
        function(e) { date_form.removeView(e.config["id"]); }
    );
    if (_status["date_description"]) {
        _status["date_description"].forEach(el => {
            date_form.addView({
                view: "template", template: el["description"],
                autoheight: true, borderless: true, type: "clean",
                css: {"text-align": "center", "margin": "10px"}
            });
        });
    }
    date_form.refresh();
}

function updateStatus() {
    var promise = webix.ajax().get(URL_STATUS);
    promise.then(data => {
        var _status = data.json();
        now.setFullYear(_status["year"], _status["month"] - 1, _status["day"]);
        now.setHours(_status["hour"], _status["minute"], _status["second"]);
        updateClock(now);
        updateTimeStatus(_status);
        updateCalendar(now);
        updateDateStatus(_status);
    }).fail(err => {
        webix.message({
            text: gettext("Failed to retrieve date/time info from server"),
            type: "error",
            expire: messageExpireTime,
            id: "failed_status_info_msg"
        });
        updateTimeStatus({});
        updateDateStatus({});
    });
}

//
// Start-up
//
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

/*
Schoolmate - school management system
Copyright (C) 2018-2022  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>

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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//
// General
//
var csrfToken = getCookie("csrftoken");
var headers = {
    "X-CSRFToken": csrfToken,
    "Content-Type": "application/json"
};

var messageExpireTime = 3000;

//
// Widget description
//
var baseLayout = {
    view: "layout", id: "base_layout", type: "clean",
    responsive: true, borderless: true, rows: [
        {id: "b_header"},
        {id: "b_body"},
        {id: "b_footer", height: 1}
    ]
};

//
// UI init
//
webix.ui(baseLayout);

var base_layout = $$("base_layout");
var b_header = $$("b_header");
var b_body = $$("b_body");
var c_footer = $$("c_footer");

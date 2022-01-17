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

//
// General
//
var URL_RECORDS = "/notebook/records/";

var max_chars = 254;

//
// Widget description
//
var notesList = {
    view: "list", id: "notes_list", layout: "y", borderless: false,
    multiselect: false, scroll: "y", select: true, url: URL_RECORDS,
    template: function(obj) {
        var dt = new Date(obj.date_modified);
        return "<div style='flex-direction:column;'>"+
               "<div style='white-space:nowrap;'>"+obj.title+"</div>"+
               "<div style='white-space:nowrap;font-size:13px;font-style:italic;'>"+
               ""+webix.i18n.fullDateFormatStr(dt)+"</div>"+
               "</div>"
    }, type: {height: "auto"}, datatype: "json", data: [],
    on: {
        onLoadError: function(err) {
            webix.message({
                text: gettext("Failed to get notebook"),
                type: "error",
                expire: messageExpireTime,
                id: "failed_get_notebook_msg"
            });
        }
    }
};

var createButton = {
    view: "icon", id: "create_button", align: "center",
    icon: "mdi mdi-note-plus-outline", css: "actionButton",
    tooltip: gettext("Create note")
};
var saveButton = {
    view: "icon", id: "save_button", align: "center",
    icon: "mdi mdi-note-check-outline", css: "actionButton",
    tooltip: gettext("Save note")
};
var closeButton = {
    view: "icon", id: "close_button", align: "center",
    icon: "mdi mdi-note-remove-outline", css: "actionButton",
    tooltip: gettext("Close note")
};
var deleteButton = {
    view: "icon", id: "delete_button", align: "center", pk: -1,
    icon: "mdi mdi-note-off-outline", css: "actionButton",
    tooltip: gettext("Delete note")
};
var titleText = {
    view: "text", name: "title_text", id: "title_text", borderless: false,
    placeholder: gettext("Title / name of this note"), inputAlign: "left",
    validate: function() {
        _title = this.getValue();
        if (_title.length > max_chars) {
            return false;
        } else {
            return true;
        }
    }, changed: false,
    invalidMessage: gettext("Max number of characters – ")+max_chars.toString()
};
var actionToolbar = {
    view: "layout", id: "action_layout", type: "line", cols: [
        createButton,
        saveButton,
        closeButton,
        deleteButton,
        titleText
    ]
};
var textEditor = {
    view: "ckeditor5", id: "text_editor", mode: "document",
    pk: -1, changed: false
};

var notebookLayout = {
    view: "layout", id: "notebook_layout", type: "line", borderless: false,
    cols: [
        {
            view: "layout", id: "list_layout", type: "clean", gravity: 2,
            rows: [
                notesList
            ]
        },
        {
            view: "layout", id: "list_layout", type: "clean", gravity: 7,
            rows: [
                actionToolbar,
                textEditor
            ]
        }
    ]
};

//
// UI init
//
webix.ui(notebookLayout, main_layout, m_body);

var notes_list = $$("notes_list");

var create_button = $$("create_button");
var save_button = $$("save_button");
var close_button = $$("close_button");
var delete_button = $$("delete_button");
var title_text = $$("title_text");

var text_editor = $$("text_editor");
var text_editor_api = null;
text_editor.getEditor(true).then(editor => {
    text_editor_api = editor;
    text_editor_api.model.document.on('change:data', () => {
        text_editor.config.changed = true;
        save_button.enable();
    });
});

//
// UI logic
//
function findItem(pk) {
    return notes_list.find(function(obj) {
        return obj.pk === pk;
    }, true);
}

function updateNote() {
    var pk = text_editor.config.pk;
    var response = webix.ajax().sync().headers(headers).patch(
        URL_RECORDS+pk.toString()+"/", {
            "pk": pk,
            "title": title_text.getValue(),
            "text": text_editor_api.getData()
        }
    );
    if (response.status < 400) {
        var r = webix.ajax().sync().get(notes_list.config.url);
        notes_list.parse(JSON.parse(r.responseText), "json", true);
        notes_list.select(findItem(pk).id);
        save_button.disable();
        title_text.config.changed = false;
        text_editor.config.changed = false;
        return true;
    } else {
        webix.message({
            text: gettext("Failed to save current note"),
            type: "error",
            expire: messageExpireTime,
            id: "failed_save_note_msg"
        });
        return false;
    }
}

function confirmSave()
{
    if (window.confirm(gettext("Save changes?"))) {
        return updateNote();
    } else {
        return true;
    }
}
function canContinue() {
    return (text_editor.config.changed || title_text.config.changed)
        ? confirmSave() : true;
}

function createNote() {
    if (!canContinue()) return;
    var promise = webix.ajax().headers(headers).post(URL_RECORDS, {
        "title": title_text.getValue(),
        "text": ""
    });
    promise.then(data => {
        _data = data.json();
        title_text.config.changed = false;
        title_text.enable();
        text_editor.config.pk = _data.pk;
        text_editor_api.setData(_data.text);
        text_editor.config.changed = false;
        text_editor.enable();
        var id = notes_list.add({
            pk: _data.pk,
            date_modified: _data.date_modified,
            title: _data.title
        }, 0);
        notes_list.select(id);
        create_button.disable();
        save_button.enable();
        close_button.enable();
        delete_button.enable();
    }).fail(err => {
        webix.message({
            text: gettext("Failed to create note"),
            type: "error",
            expire: messageExpireTime,
            id: "failed_create_note_msg"
        });
    });
}

function retrieveNote(id, e, node) {
    var pk = notes_list.getItem(id).pk;
    if (!canContinue()) return;
    notes_list.select(findItem(pk).id);
    var promise = webix.ajax().get(URL_RECORDS + pk.toString());
    promise.then(data => {
        _data = data.json();
        title_text.setValue(_data.title);
        title_text.config.changed = false;
        title_text.enable();
        text_editor.config.pk = _data.pk;
        text_editor_api.setData(_data.text);
        text_editor.config.changed = false;
        text_editor.enable();
        create_button.disable();
        save_button.enable();
        close_button.enable();
        delete_button.enable();
    }).fail(err => {
        webix.message({
            text: gettext("Failed to retrieve note"),
            type: "error",
            expire: messageExpireTime,
            id: "failed_retrieve_note_msg"
        });
    });
}

function closeNote(confirm=true) {
    if (confirm) {
        if (!canContinue()) return;
    }
    title_text.setValue("");
    title_text.config.changed = false;
    title_text.disable();
    text_editor.config.pk = -1;
    text_editor_api.setData("");
    text_editor.config.changed = false;
    text_editor.disable();
    create_button.enable();
    save_button.disable();
    close_button.disable();
    delete_button.enable();
}

function deleteNote() {
    var pk = delete_button.config.pk;
    if (pk === text_editor.config.pk) {
        if (!window.confirm(gettext("Delete current note?"))) return;
    }
    var promise = webix.ajax().headers(headers).del(URL_RECORDS+pk.toString()+"/");
    promise.then(data => {
        var id = notes_list.getSelectedId();
        notes_list.remove(id);
        closeNote(false);
        delete_button.disable();
    }).fail(err => {
        webix.message({
            text: gettext("Failed to delete selected note"),
            type: "error",
            expire: messageExpireTime,
            id: "failed_delete_note_msg"
        });
    });
}

//
// Event handling
//
create_button.attachEvent("onItemClick", createNote);
save_button.attachEvent("onItemClick", updateNote);
close_button.attachEvent("onItemClick", closeNote);
delete_button.attachEvent("onItemClick", deleteNote);

notes_list.attachEvent("onAfterSelect", function(id, e, node) {
    var pk = this.getItem(id).pk;
    delete_button.config.pk = pk;
    delete_button.enable();
});
notes_list.attachEvent("onItemDblClick", retrieveNote);

title_text.attachEvent("onChange", function() {this.config.changed = true});

//
// Start-up
//
save_button.disable();
delete_button.disable();
close_button.disable();

title_text.disable();
text_editor.disable();

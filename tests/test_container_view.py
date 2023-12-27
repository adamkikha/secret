import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from src.view.view import View
from src.view.container_view import (
    ContMenuBar,
    RecordsWindow,
)


def test_master_key_frame():
    """test the master key frame attributes"""
    secret_root = View()
    master_key_frame = secret_root.container_view.master_key_frame

    child_widgets = master_key_frame.winfo_children()

    child_types = [ctk.CTkEntry, ctk.CTkLabel, ctk.CTkButton, ctk.CTkButton]
    child_btn_txt = ["", "Confirm", "Back"]

    for i, widget in enumerate(child_widgets):
        assert isinstance(widget, child_types[i])

    for i in range(len(child_btn_txt)):
        assert child_widgets[i + 1].cget("text") == child_btn_txt[i]

    secret_root.destroy()


def test_container_display_frame():
    """test the passwords display frame attributes"""
    secret_root = View()

    passwords_display_frame = secret_root.container_view.container_display_frame

    child_widgets = passwords_display_frame.winfo_children()
    child_types = [
        ctk.CTkButton,
        ctk.CTkEntry,
        ctk.CTkEntry,
        ctk.CTkEntry,
        ctk.CTkEntry,
        ctk.CTkEntry,
        ctk.CTkButton,
        ttk.Treeview,
    ]

    assert len(child_widgets) == 8
    assert child_widgets[0].cget("text") == "+ Add"

    for i, widget in enumerate(child_widgets):
        assert isinstance(widget, child_types[i])

    secret_root.destroy()


def test_scroll_bar():
    """test the scroll bar attributes"""

    secret_root = View()

    frame = tk.Frame(secret_root, borderwidth=2, relief="solid")
    menu_bar = ContMenuBar(secret_root.container_view, frame)

    child_cascades = menu_bar.menubar.winfo_children()
    menu_bar_item = 1
    cascade_labels = ["File", "Settings"]
    child_sub_labels = [["New", "Open", "Lock", "Close"], [], [], []]

    assert len(child_cascades) == menu_bar_item

    for i, cascade in enumerate(child_cascades):
        assert (
            menu_bar.menubar.entrycget(cascade_labels[i], "label") == cascade_labels[i]
        )

    secret_root.destroy()


def test_records_frame():
    secret_root = View()
    headers = ["ID", "Filename", "Tag", "Notes", "Size", "Modification date"]
    record_window = RecordsWindow(secret_root, None)
    widgets = record_window.children
    widgets_type = list(widgets.values())
    types_dict = {}
    assert len(widgets) == 11
    for wid in widgets_type:
        if type(wid) in types_dict:
            types_dict[type(wid)] += 1
        else:
            types_dict[type(wid)] = 1

    for key, value in types_dict.items():
        if isinstance(key, ctk.CTkLabel):
            assert value == 9
        elif isinstance(key, ctk.CTkEntry):
            assert value == 4
        elif isinstance(key, tk.Text):
            assert value == 1
        elif isinstance(key, ctk.CTkButton):
            assert value == 1

    record_window.destroy()
    secret_root.destroy()

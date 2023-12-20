import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from src.view.view import (
    Secret,
    InitFrame,
    PassMKFrame,
    PasswordsDisplayFrame,
    PassMenuBar,
)


def test_root():
    """test the root attributes"""
    secret_root = Secret()
    secret_root.set_geometry()

    width = 800
    height = 700
    title = "Secret"

    secret_root_width = secret_root.winfo_width()
    secret_root_height = secret_root.winfo_height()
    secret_root_title = secret_root.title()

    assert (
        secret_root_width == width
    ), f"Width should be {width}, but got {secret_root_width}"

    assert (
        secret_root_height == height
    ), f"Width should be {height}, but got {secret_root_height}"

    assert (
        secret_root_title == title
    ), f"Title should be {title}, but got {secret_root_title}"

    secret_root.destroy()



def test_root_frames():
    """test the root frames"""

    secret_root = Secret()

    assert issubclass(Secret, ctk.CTk)
    assert issubclass(InitFrame, ctk.CTkFrame)
    assert issubclass(PassMKFrame, ctk.CTkFrame)
    assert issubclass(PasswordsDisplayFrame, ctk.CTkFrame)

    assert isinstance(secret_root.init_frame, InitFrame)
    assert isinstance(secret_root.master_key_frame, PassMKFrame)
    assert isinstance(secret_root.passwords_display_frame, PasswordsDisplayFrame)

    secret_root.destroy()



def test_init_frame():
    """test the init frame attributes"""

    secret_root = Secret()
    init_frame = secret_root.init_frame

    btn1_text = "Passwords"
    btn2_text = "Files Container"

    child_widgets = init_frame.winfo_children()

    assert isinstance(child_widgets[0], ctk.CTkButton)

    assert isinstance(child_widgets[1], ctk.CTkButton)

    assert (
        child_widgets[0].cget("text") == btn1_text
    ), f"The button text should be '{btn1_text}'"

    assert (
        child_widgets[1].cget("text") == btn2_text
    ), f"The button text should be '{btn1_text}'"

    secret_root.destroy()



def test_master_key_frame():
    """test the master key frame attributes"""
    secret_root = Secret()
    master_key_frame = secret_root.master_key_frame

    child_widgets = master_key_frame.winfo_children()

    child_types = [ctk.CTkEntry, ctk.CTkButton, ctk.CTkButton]
    child_btn_txt = ["Confirm", "Back"]

    for i, widget in enumerate(child_widgets):
        assert isinstance(widget, child_types[i])

    for i in range(len(child_btn_txt)):
        print(child_widgets[i + 1].cget("text"), child_btn_txt[i])
        assert child_widgets[i + 1].cget("text") == child_btn_txt[i]

    secret_root.destroy()



def test_passwords_display_frame():
    """test the passwords display frame attributes"""
    secret_root = Secret()

    passwords_display_frame = secret_root.passwords_display_frame

    child_widgets = passwords_display_frame.winfo_children()
    child_types = [ctk.CTkButton, ttk.Treeview]

    assert child_widgets[0].cget("text") == "+ Add"
    for i, widget in enumerate(child_widgets):
        assert isinstance(widget, child_types[i])

    secret_root.destroy()



def test_scroll_bar():
    """test the scroll bar attributes"""
    secret_root = Secret()
    frame = tk.Frame(secret_root, borderwidth=2, relief="solid")
    menu_bar = PassMenuBar(secret_root, frame)

    child_cascades = menu_bar.menubar.winfo_children()
    menu_bar_item = 4
    cascade_labels = ["File", "View", "Tools", "Settings"]
    child_sub_labels = [["New", "Open", "Lock", "Close"], [], [], []]
    
    assert len(child_cascades) == menu_bar_item
    
    for i, cascade in enumerate(child_cascades):
        assert menu_bar.menubar.entrycget(cascade_labels[i],'label') ==  cascade_labels[i]
        print(cascade.winfo_children())

    secret_root.destroy()

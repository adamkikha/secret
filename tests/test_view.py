import customtkinter as ctk
from src.view.view import View, InitFrame
from src.view.passwords_view import (
    PassMKFrame,
    PasswordsDisplayFrame,
)


def test_root():
    """test the root attributes"""
    secret_root = View()
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

    secret_root = View()

    assert issubclass(View, ctk.CTk)
    assert issubclass(InitFrame, ctk.CTkFrame)
    assert issubclass(PassMKFrame, ctk.CTkFrame)
    assert issubclass(PasswordsDisplayFrame, ctk.CTkFrame)

    assert isinstance(secret_root.init_frame, InitFrame)
    assert isinstance(secret_root.passwords_view.master_key_frame, PassMKFrame)
    assert isinstance(
        secret_root.passwords_view.passwords_display_frame, PasswordsDisplayFrame
    )

    secret_root.destroy()


def test_init_frame():
    """test the init frame attributes"""

    secret_root = View()
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

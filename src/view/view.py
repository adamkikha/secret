import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import customtkinter as ctk


class InitFrame(ctk.CTkFrame):
    def __init__(self, controller):
        ctk.CTkFrame.__init__(self, controller)
        self.controller = controller

        # ---------- widgets ----------
        self.frame = ctk.CTkFrame(self.controller)

        self.secret_lbl = ctk.CTkLabel(
            self.frame, text="Secret", font=("Trebuchet MS", 40, "bold")
        )
        self.secret_lbl.pack()

        self.passwords_btn = ctk.CTkButton(
            master=self,
            width=180,
            height=40,
            text="Passwords",
            font=("Trebuchet MS", 20, "bold"),
            command=self.passwords_btn_function,
        )
        self.passwords_btn.place(anchor="c", relx=0.5, rely=0.4)

        self.files_btn = ctk.CTkButton(
            master=self,
            width=180,
            height=40,
            text="Files Container",
            font=("Trebuchet MS", 20, "bold"),
            command=self.files_btn_function,
        )
        self.files_btn.place(anchor="c", relx=0.5, rely=0.5)
        # ---------------------------

    def display(self):
        self.pack(pady=10, padx=10, fill="both", expand=True)

    def passwords_btn_function(self):
        self.pack_forget()
        self.controller.passwords_display_frame.display()

    def files_btn_function(self):
        pass


class PassMKFrame(ctk.CTkFrame):
    def __init__(self, controller):
        ctk.CTkFrame.__init__(self, controller)

        self.controller = controller
        self.new_MK = True

        # ---------- widgets ----------
        # Entry for the password
        self.mk_ent = ctk.CTkEntry(
            master=self,
            width=200,
            height=30,
            show="*",
            font=("Trebuchet MS", 15),
            placeholder_text="Master Key",
        )
        self.mk_ent.place(anchor="c", relx=0.5, rely=0.4)

        # confiem buton
        self.confirm_btn = ctk.CTkButton(
            master=self,
            width=150,
            height=30,
            text="Confirm",
            font=("Trebuchet MS", 20, "bold"),
            command=self.confirm_btn_com,
        )
        self.confirm_btn.place(anchor="c", relx=0.5, rely=0.5)

        # back button
        back_btn = ctk.CTkButton(
            master=self,
            width=80,
            height=30,
            text="Back",
            font=("Trebuchet MS", 15, "bold"),
            command=self.back_btn_com,
        )
        back_btn.place(anchor="c", relx=0.5, rely=0.6)

    def display(self, new_MK=True):
        self.focus_set()  # changing the focus from the entry when switching back to the same frame
        self.new_MK = new_MK
        self.pack(pady=10, padx=10, fill="both", expand=True)

    def back_btn_com(self):
        self.pack_forget()
        self.controller.passwords_display_frame.display()

    def confirm_btn_com(self):
        self.mk_ent.delete(0, tk.END)
        # self.mk_ent.configure(placeholder_text="Master Key")
        print(self.mk_ent.get())
        if self.new_MK:
            self.pop_up_window("Key set successfully!!", "green", "Success!")
            self.pack_forget()
            self.controller.master_key = self.mk_ent.get()
            self.controller.passwords_display_frame.display()
        else:
            result = self.controller.check_MK(self.mk_ent.get())
            if result:
                self.pop_up_window("File opened successfully!!", "green", "Success!")
                self.pack_forget()
                self.controller.passwords_display_frame.display()
            else:
                self.pop_up_window("Wrong password!!", "red", "Failed!")

    def pop_up_window(self, msg_text, text_color, win_title):
        pop_up_window = ctk.CTkToplevel(self)
        pop_up_window.title(win_title)
        width = 300
        height = 100

        # pop up window geometry
        pop_up_window.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        pop_up_window.geometry(f"{width}x{height}+{x}+{y}")

        # message label
        msg_lbl = ctk.CTkLabel(
            pop_up_window,
            text=msg_text,
            font=("Arial", 16, "bold"),
            text_color=text_color,
        )
        msg_lbl.pack(pady=10)

        # ok button
        ok_button = ctk.CTkButton(
            pop_up_window, text="OK", command=pop_up_window.destroy
        )
        ok_button.pack(pady=10)


class PassMenuBar(tk.Menu):
    """
    Custom menubar for the passwords container
    """

    def __init__(self, controller, frame):
        super().__init__(controller)
        self.controller = controller
        self.frame = frame
        self.menubar = tk.Menu(controller, font=("Trebuchet MS", 100, "bold"))
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(
            label="New", accelerator="Ctrl+N", command=self.new_file_clicked
        )
        self.file_menu.add_command(
            label="Open", accelerator="Ctrl+O", command=self.open_file_clicked
        )
        self.file_menu.add_command(
            label="Lock", accelerator="Ctrl+L", command=self.lock_file_clicked
        )
        self.file_menu.add_command(
            label="Close", accelerator="Ctrl+E", command=self.close_file_clicked
        )

        self.view_menu = tk.Menu(self.menubar, tearoff=False)

        self.tools_menu = tk.Menu(self.menubar, tearoff=False)

        self.settings_menu = tk.Menu(self.menubar, tearoff=False)

        self.menubar.add_cascade(menu=self.file_menu, label="File")
        self.menubar.add_cascade(menu=self.view_menu, label="View")
        self.menubar.add_cascade(menu=self.view_menu, label="Tools")
        self.menubar.add_cascade(menu=self.settings_menu, label="Settings")

    def display(self):
        self.controller.config(menu=self.menubar)

    def new_file_clicked(self):
        self.controller.config(menu="")
        self.frame.pack_forget()
        self.controller.master_key_frame.display()

    def open_file_clicked(self):
        self.controller.config(menu="")
        self.frame.pack_forget()
        self.controller.open_file()
        self.controller.master_key_frame.display(False)

    def lock_file_clicked(self):
        self.controller.passwords_display_frame.clear_data()
        self.controller.master_key = None
        self.controller.passwords_enc_data = None
        self.controller.passwords_display_frame.pack_forget()
        self.controller.master_key_frame.display()

    def close_file_clicked(self):
        self.controller.config(menu="")
        self.controller.master_key = None
        self.controller.passwords_enc_data = None
        self.controller.passwords_dec_data = None
        self.frame.pack_forget()
        self.controller.init_frame.display()


class PasswordsDisplayFrame(ctk.CTkFrame):
    def __init__(self, controller):
        ctk.CTkFrame.__init__(self, controller)
        self.controller = controller
        self.menu_bar = PassMenuBar(self.controller, self)
        self.configure()
        # ---------- attributes ----------
        self.headers = ("ID", "Username", "password", "Tag", "URL")
        self.headers_size = (30, 150, 200, 50, 200)
        self.center_header_indeces = [4]
        # ---------- widgets ----------

        # Add button
        self.add_btn = ctk.CTkButton(
            master=self,
            width=100,
            height=20,
            text="+ Add",
            font=("Trebuchet MS", 15, "bold"),
            corner_radius=0,
            command=self.add_btn_com,
        )
        self.add_btn.pack(anchor="w", padx=0, pady=(20, 10))

        # data container
        self.data_tree = ttk.Treeview(self, columns=self.headers, show="headings")
        self.data_tree.pack(pady=0, fill="both", expand=True)

        # adding events to the data container
        self.data_tree.bind("<Double-1>", self.on_double_click_evt)
        self.data_tree.bind("<Button-3>", self.on_right_click_evt)

        # scroll bar
        self.scroll_bar = ctk.CTkScrollbar(
            master=self.data_tree, orientation="vertical", command=self.data_tree.yview
        )
        self.scroll_bar.pack(side="right", pady=5, fill="y")
        self.data_tree.configure(yscrollcommand=self.scroll_bar.set)

        # -----------------------------
        # Define column headings
        for i, col in enumerate(self.headers):
            self.data_tree.heading(col, text=col)
            if i in self.center_header_indeces:
                self.data_tree.column(col, width=self.headers_size[i], anchor="center")
            else:
                self.data_tree.column(col, width=self.headers_size[i])

    def display(self):
        self.menu_bar.display()
        self.pack(pady=10, padx=10, fill="both", expand=True)
        if self.controller.passwords_enc_data:
            self.fill_table(self.controller.passwords_enc_data)

    def fill_table(self, data):
        for row in data:
            self.data_tree.insert("", "end", values=row)

    def clear_data(self):
        for item_id in self.data_tree.get_children():
            self.data_tree.delete(item_id)

    def on_double_click_evt(self, event):
        item_id = self.data_tree.selection()[0]
        values = self.data_tree.item(item_id, "values")
        print(values)
        self.view_record(values)

    def view_record(self, record_values):
        top_level = ctk.CTkToplevel()
        top_level.title("View")
        self.top_level_windows_geometry(top_level, 400, 350)
        top_level.grab_set()
        top_level.protocol(
            "WM_DELETE_WINDOW", lambda: self.on_top_level_close(top_level)
        )
        for header, value in zip(self.headers, record_values):
            label = ctk.CTkLabel(top_level, text=f"{header}: {value}")
            label.pack()

    def top_level_windows_geometry(self, top_level_wind, width, height):
        top_level_wind.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        top_level_wind.geometry(f"{width}x{height}+{x}+{y}")

    def on_top_level_close(self, top_level_wind):
        # Release the grab when the top-level window is closed
        top_level_wind.grab_release()
        top_level_wind.destroy()

    def on_right_click_evt(self, event):
        # Identify the item and column that were right-clicked
        record_id = self.data_tree.identify_row(event.y)
        col_id = int(self.data_tree.identify_column(event.x).split("#")[1])
        if record_id and col_id:
            record_values = self.data_tree.item(record_id, "values")
            clicked_text = record_values[col_id - 1]

            context_menu = tk.Menu(self.data_tree, tearoff=0)
            context_menu.add_command(
                label="Copy", command=lambda: self.copy_text(clicked_text)
            )
            context_menu.post(event.x_root, event.y_root)  # close the context_menu

    def copy_text(self, text):
        self.data_tree.clipboard_clear()
        self.data_tree.clipboard_append(text)

    def add_btn_com(self):
        pass


class Secret(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secret")
        self.width = 800
        self.height = 700
        self.set_geometry()

        self.master_key = None
        self.passwords_file_path = None
        self.passwords_enc_data = None
        self.passwords_dec_data = None
        # ---------- frames ----------

        self.init_frame = InitFrame(self)
        self.master_key_frame = PassMKFrame(self)
        # passwords
        self.passwords_display_frame = PasswordsDisplayFrame(self)
        # files container
        self.files_display_frame = None
        # --------------------------------

        self.init_frame.display()

    def set_geometry(self):
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def open_file(self):
        # TODO: file type should be changed to a specific type
        self.passwords_file_path = filedialog.askopenfilename(
            title="Open File", filetypes=[("All files", "*.*")], initialdir="./"
        )


    def check_MK(self, master_key):
        return True
    
    


if __name__ == "__main__":
    # TODO: the following two lines should be moved to the setting window
    ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    app = Secret()
    app.mainloop()





import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import filedialog
from src.utils import TimeOracle
from src.model.password_record import PasswordRecord


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
            command=None,
            state="disabled",
        )
        self.files_btn.place(anchor="c", relx=0.5, rely=0.5)
        # ---------------------------

    def display(self):
        self.pack(pady=10, padx=10, fill="both", expand=True)

    def passwords_btn_function(self):
        self.pack_forget()
        self.controller.passwords_display_frame.display()


class RecordsWindow(ctk.CTkToplevel):
    """frame used for add, view, and edit the records"""

    def __init__(self, controller, table_wid, headers):
        """_summary_

        Args:
            table_wid (_type_): _description_
            headers (_type_): _description_
            non_editable_headers (_type_): _description_
            "Username", "password", "Tag", "URL", "Notes", "password modification date","Record modification date", "ID"
        """
        ctk.CTkToplevel.__init__(self)

        self.title("View")
        self.set_geometry(600, 550)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.ent_fields = []
        self.controller = controller
        self.data_table = table_wid
        self.record_id = None
        self.record_inter_id = None
        self.record_orig_data = None
        self.dates = []
        # ---------- widgets ----------
        i = 0
        for i, header in enumerate(headers[1:-3]):
            # header label
            header_label = ctk.CTkLabel(self, text=header + ":")
            header_label.grid(row=i, column=0, padx=50, pady=5, sticky="w")
            # data entry
            data_entry = ctk.CTkEntry(self, width=250)
            data_entry.grid(row=i, column=1, padx=5, pady=5)
            # saving the entry fields in an array as a class variable
            self.ent_fields.append(data_entry)

        for header in headers[-2:]:
            i += 1  # update the next grid row
            # header label
            header_label = ctk.CTkLabel(self, text=header + ":")
            header_label.grid(row=i, column=0, padx=50, pady=5, sticky="w")
            # data label
            data_entry = ctk.CTkLabel(self, text="", width=250)
            data_entry.grid(row=i, column=1, padx=5, pady=5)
            # saving the date widgets in an array as a class variable
            self.dates.append(data_entry)

        i += 1  # update the next grid row
        # notes label
        notes_label = ctk.CTkLabel(self, text=headers[-3] + ":")
        notes_label.grid(row=i, column=0, padx=50, pady=5, sticky="w")
        # notes entry
        self.notes_ent = tk.Text(self, wrap="word", width=40, height=10)
        self.notes_ent.grid(row=i + 1, column=1, padx=5, pady=5)

        # actions button
        self.btn = ctk.CTkButton(
            master=self,
            width=150,
            height=30,
            text="Confirm",
            font=("Trebuchet MS", 20, "bold"),
            command=self.btn_add_record_com,
        )
        self.btn.place(anchor="c", relx=0.5, rely=0.9)
        # -----------------------------

    def set_geometry(self, width, height):
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def read_ent_fields(self):
        record = []
        for wid in self.ent_fields:
            record.append(wid.get())
            # wid.delete(0, tk.END)
        record.append(self.notes_ent.get("1.0", "end-1c"))
        return record

    def view_record(self, record, record_inter_id):
        self.record_id = record[-1]
        record.pop(0)  # get rid of the index
        record.pop()  # get rid of the id
        self.record_inter_id = record_inter_id
        for i, value in enumerate(record[:-3]):
            self.ent_fields[i].insert(0, str(value))
            self.ent_fields[i].configure(state="readonly", fg_color="#f2f2f2")

        self.notes_ent.insert("1.0", record[-3])
        self.notes_ent.config(state="disabled", bg="#f2f2f2")

        self.dates[0].configure(text=record[-2])
        self.dates[1].configure(text=record[-1])

        self.btn.configure(text="Edit", command=self.btn_edit_com)

    def btn_edit_com(self):
        # save the original data
        self.record_orig_data = self.read_ent_fields()
        # make the fields editable
        for wid in self.ent_fields:
            wid.configure(state="normal", fg_color="#ffffff")
        self.notes_ent.config(state="normal", bg="#ffffff")
        # change the button text and command
        self.btn.configure(text="Confirm", command=self.btn_confirm_edit_com)

    def btn_confirm_edit_com(self):
        record = self.read_ent_fields()
        # print("old:", self.record_orig_data)
        # print("new:", record)

        # send the updates to the GUI controller
        self.controller.edit_record(record, self.record_id)
        self.destroy()

    def btn_add_record_com(self):
        new_record = self.read_ent_fields()
        # send the updates to the GUI controller
        self.controller.add_record(new_record)
        # add the record to the table
        # self.data_table.insert("", "end", values=new_record)
        self.destroy()

    def on_close(self):
        # Release the grab when the window is closed
        self.grab_release()
        self.destroy()


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
        # if self.controller.passwords_file_path:
        self.controller.passwords_display_frame.menu_bar.close_file_clicked(save=False)
        # else:
        #     self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
        #     "Open", state="normal"
        #     )
        #     self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
        #     "New", state="normal"
        #     )

        # self.controller.passwords_display_frame.display()
        self.pack_forget()

    def confirm_btn_com(self):
        # self.mk_ent.configure(placeholder_text="Master Key")
        # print(self.mk_ent.get())

        if self.new_MK:
            self.controller.master_key = self.mk_ent.get()
            self.controller.save_path()
            self.controller.passwords_display_frame.display()
            self.pop_up_window("Key set successfully!!", "green", "Success!")
            self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                "Lock", state="normal"
            )
            self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                "Close", state="normal"
            )
            self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                "Save", state="normal"
            )
            self.pack_forget()
        else:
            result = self.controller.check_MK(self.mk_ent.get())
            if result:
                self.pop_up_window("File opened successfully!!", "green", "Success!")
                self.controller.passwords_display_frame.display()
                self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                    "Lock", state="normal"
                )
                self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                    "Close", state="normal"
                )
                self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                    "Save", state="normal"
                )
                self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                    "Open", state="disabled"
                )
                self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                    "New", state="disabled"
                )
                self.pack_forget()
            else:
                self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                    "Open", state="normal"
                )
                self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                    "New", state="normal"
                )
                self.pop_up_window("Wrong password!!", "red", "Failed!")
        self.mk_ent.delete(0, tk.END)

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
            label="Save",
            accelerator="Ctrl+S",
            state="disabled",
            command=self.save_file_clicked,
        )
        self.file_menu.add_command(
            label="Lock",
            accelerator="Ctrl+L",
            state="disabled",
            command=self.lock_file_clicked,
        )

        self.file_menu.add_command(
            label="Close",
            accelerator="Ctrl+E",
            state="disabled",
            command=self.close_file_clicked,
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
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Open", state="disabled"
        )
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "New", state="disabled"
        )
        self.controller.config(menu="")
        self.frame.pack_forget()
        self.controller.master_key_frame.display()

    def open_file_clicked(self):
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Open", state="disabled"
        )
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "New", state="disabled"
        )
        if not self.controller.passwords_file_path:
            self.controller.pick_file()
            if not self.controller.passwords_file_path:  # user didn't pick file
                self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                    "Open", state="normal"
                )
                self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                    "New", state="normal"
                )
                self.pack_forget()
                self.controller.passwords_display_frame.display()
                return

        self.controller.config(menu="")
        self.frame.pack_forget()
        self.controller.master_key_frame.display(False)

    def save_file_clicked(self):
        self.controller.passwords_controller.save_file()

    def lock_file_clicked(self):
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Lock", state="disabled"
        )

        self.controller.passwords_controller.close_file(save=True)

        self.controller.passwords_display_frame.pack_forget()
        self.controller.master_key = None
        self.controller.passwords_dec_data = []
        self.controller.master_key_frame.display(False)

    def unlock_file_clicked(self):
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Lock", state="normal"
        )
        # TODO: pop up window for lock

    def close_file_clicked(self, save=True):
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Lock", state="disabled"
        )
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Save", state="disabled"
        )
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Close", state="disabled"
        )
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Open", state="normal"
        )
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "New", state="normal"
        )
        self.controller.passwords_controller.close_file(save)
        self.controller.config(menu="")
        self.controller.master_key = None
        self.controller.passwords_dec_data = []
        self.controller.passwords_file_path = None
        self.frame.pack_forget()
        self.controller.init_frame.display()


class PasswordsDisplayFrame(ctk.CTkFrame):
    def __init__(self, controller):
        ctk.CTkFrame.__init__(self, controller)

        self.controller = controller
        self.menu_bar = PassMenuBar(self.controller, self)

        # ---------- attributes ----------
        self.headers = ["ID", "Username", "password", "Tag", "URL"]
        self.hidden_headers = [
            "Notes",
            "password modification date",
            "Record modification date",
        ]

        self.headers_size = (10, 150, 200, 50, 220)
        self.center_header_indeces = [0, 3]
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
        self.add_btn.configure(state="disabled")
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
        if self.controller.master_key:
            self.add_btn.configure(state="normal")
        else:
            self.add_btn.configure(state="disabled")
        self.menu_bar.display()
        self.pack(pady=10, padx=10, fill="both", expand=True)
        self.clear_data()
        self.fill_table(self.controller.passwords_dec_data)

    def fill_table(self, data: list[PasswordRecord]):
        for i, row in enumerate(data):
            table_row = [
                str(i + 1),
                row.username,
                row.password,
                row.tag,
                row.url,
                row.notes,
                TimeOracle.get_readable_time(row.pass_mdate),
                TimeOracle.get_readable_time(row.record_mdate),
                row.id,
            ]
            self.data_tree.insert("", "end", values=table_row)

    def clear_data(self):
        for item_id in self.data_tree.get_children():
            self.data_tree.delete(item_id)

    def on_double_click_evt(self, event):
        record_inter_id = self.data_tree.selection()[0]
        values = list(self.data_tree.item(record_inter_id, "values"))
        self.view_record(values, record_inter_id)

    def view_record(self, record_values, record_inter_id):
        record_window = RecordsWindow(
            self.controller, self.data_tree, self.headers + self.hidden_headers
        )
        record_window.view_record(record_values, record_inter_id)
        # for header, value in zip(self.headers, record_values):
        #     label = ctk.CTkLabel(record_window, text=f"{header}: {value}")
        #     label.pack()

    def on_right_click_evt(self, event):
        # Identify the item and column that were right-clicked
        record_inter_id = self.data_tree.identify_row(event.y)
        col_id = int(self.data_tree.identify_column(event.x).split("#")[1])
        if record_inter_id and col_id:
            record_values = self.data_tree.item(record_inter_id, "values")
            clicked_text = record_values[col_id - 1]

            context_menu = tk.Menu(self.data_tree, tearoff=0)
            context_menu.add_command(
                label="Copy", command=lambda: self.copy_text(clicked_text)
            )
            context_menu.add_command(
                label="Delete", command=lambda: self.delete_record(record_values[-1])
            )
            context_menu.post(event.x_root, event.y_root)  # close the context_menu

    def copy_text(self, text):
        self.data_tree.clipboard_clear()
        self.data_tree.clipboard_append(text)

    def delete_record(self, record_id):
        self.controller.passwords_controller.delete_record(int(record_id))

    def add_btn_com(self):
        record_window = RecordsWindow(
            self.controller, self.data_tree, self.headers + self.hidden_headers
        )


class Secret(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secret")
        self.width = 800
        self.height = 700
        self.set_geometry()

        self.passwords_controller = None

        # ---------- data ----------
        self.master_key = None
        self.passwords_file_path = None
        self.passwords_dec_data = []
        # --------------------------

        # ---------- frames ----------
        # initial window
        self.init_frame = InitFrame(self)
        # master key window
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

    def pick_file(self):
        # TODO: file type should be changed to a specific type
        self.passwords_file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("All files", "*.secretpass*")],
            initialdir="./",
        )

    def save_path(self):
        self.passwords_file_path = filedialog.asksaveasfilename(
            title="Choose Destination",
            filetypes=[("All files", "*.secretpass*")],
            initialdir="./",
        )
        self.passwords_controller.create_file(self.master_key, self.passwords_file_path)

    def add_record(self, record):
        self.passwords_controller.add_record(
            record[0], record[1], record[2], record[3], record[4]
        )

    def edit_record(self, record, record_id):
        self.passwords_controller.modify_record(
            int(record_id), record[0], record[1], record[2], record[3], record[4]
        )

    def check_MK(self, master_key):
        self.master_key = master_key
        result = self.passwords_controller.open_file(
            master_key, self.passwords_file_path
        )
        return result

    def update_data(self, new_data):
        self.passwords_dec_data = new_data
        self.passwords_display_frame.display()

    def set_passwords_controller(self, controller):
        self.passwords_controller = controller


if __name__ == "__main__":
    # TODO: the following two lines should be moved to the setting window
    ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    app = Secret()
    app.mainloop()

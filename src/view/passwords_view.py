import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import filedialog
from src.utils import TimeOracle


class PassGenSettings:
    def __init__(self, container, row_index):
        self.container = container
        self.lower_case_cbox_var = tk.BooleanVar()
        self.upper_case_cbox_var = tk.BooleanVar()
        self.numbers_cbox_var = tk.BooleanVar()
        self.symbols_cbox_var = tk.BooleanVar()
        self.cbox_vars = [
            self.lower_case_cbox_var,
            self.upper_case_cbox_var,
            self.numbers_cbox_var,
            self.symbols_cbox_var,
        ]
        self.cbox_com = [
            self.btn_lower_case_cbox_clicked,
            self.btn_upper_case_cbox_clicked,
            self.btn_numbers_cbox_clicked,
            self.btn_symbols_cbox_clicked,
        ]
        self.cbox_names = [
            "Lower case letters:",
            "Upper case letters:",
            "Numbers:",
            "Symbols:",
        ]
        # password length
        row_index += 1
        length_label = ctk.CTkLabel(
            container,
            text="Password length:",
        )
        length_label.grid(row=row_index, column=0, padx=50, pady=5, sticky="w")
        self.length_entry = ctk.CTkEntry(
            container,
            width=100,
        )
        self.length_entry.grid(row=row_index, column=1, padx=10, pady=5)
        self.length_entry.bind("<FocusOut>", self.length_entry_focus_out)

        # checkboxes
        for cbox_name, cbox_var, cbox_com in zip(
            self.cbox_names, self.cbox_vars, self.cbox_com
        ):
            row_index += 1
            label = ctk.CTkLabel(container, text=cbox_name)
            label.grid(row=row_index, column=0, padx=50, pady=5, sticky="w")
            cbox = ctk.CTkCheckBox(
                master=container,
                text="",
                variable=cbox_var,
                command=cbox_com,
                onvalue=True,
                offvalue=False,
            )
            cbox.grid(row=row_index, column=1, padx=5, pady=5)

    def set_values(self):
        self.length_entry.insert("0", str(self.container.controller.settings.length))
        self.lower_case_cbox_var.set(self.container.controller.settings.lower_case)
        self.upper_case_cbox_var.set(self.container.controller.settings.upper_case)
        self.numbers_cbox_var.set(self.container.controller.settings.digits)
        self.symbols_cbox_var.set(self.container.controller.settings.symbols)

    def update_generate_pass_val(self):
        self.container.controller.passwords_controller.set_length_setting(
            int(self.length_entry.get())
        )
        self.container.controller.passwords_controller.set_lower_case_setting(
            self.lower_case_cbox_var.get()
        )
        self.container.controller.passwords_controller.set_upper_case_setting(
            self.upper_case_cbox_var.get()
        )
        self.container.controller.passwords_controller.set_digits_setting(
            self.numbers_cbox_var.get()
        )
        self.container.controller.passwords_controller.set_symbols_setting(
            self.symbols_cbox_var.get()
        )

    def length_entry_focus_out(self, event):
        self.container.controller.passwords_controller.set_length_setting(
            self.length_entry.get()
        )

    def btn_lower_case_cbox_clicked(self):
        self.container.controller.passwords_controller.set_lower_case_setting(
            self.lower_case_cbox_var.get()
        )

    def btn_upper_case_cbox_clicked(self):
        self.container.controller.passwords_controller.set_upper_case_setting(
            self.upper_case_cbox_var.get()
        )

    def btn_numbers_cbox_clicked(self):
        self.container.controller.passwords_controller.set_digits_setting(
            self.numbers_cbox_var.get()
        )

    def btn_symbols_cbox_clicked(self):
        self.container.controller.passwords_controller.set_symbols_setting(
            self.symbols_cbox_var.get()
        )


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, controller):
        ctk.CTkToplevel.__init__(self)
        self.title("Settings")
        self.set_geometry(400, 350)
        self.wait_visibility()
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.controller = controller
        # ---------- widgets ----------
        # warnings
        row_index = 0
        warn_label = ctk.CTkLabel(self, text="Passwords warnings:")
        warn_label.grid(row=row_index, column=0, padx=50, pady=5, sticky="w")

        self.warn_cbox_var = tk.BooleanVar()
        self.warn_cbox = ctk.CTkCheckBox(
            master=self,
            text="",
            variable=self.warn_cbox_var,
            command=self.cbox_warn_com,
            onvalue=True,
            offvalue=False,
        )
        self.warn_cbox.grid(row=row_index, column=1, padx=5, pady=5)

        self.warn_entry = ctk.CTkEntry(
            self, width=50, fg_color="#f2f2f2", state="readonly"
        )
        self.warn_entry.place(anchor="c", relx=0.85, rely=0.05)
        self.warn_entry.bind("<FocusOut>", self.warn_entry_focus_out)

        # backup
        row_index += 1
        backup_label = ctk.CTkLabel(self, text="Backups:")
        backup_label.grid(row=row_index, column=0, padx=50, pady=5, sticky="w")

        self.backup_entry = ctk.CTkEntry(
            self,
            width=100,
        )
        self.backup_entry.grid(row=row_index, column=1, padx=10, pady=5)

        self.pass_gen_settings = PassGenSettings(self, row_index)

        # -----------------------------
        self.set_settings()

    def set_geometry(self, width, height):
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def set_settings(self):
        self.warn_cbox_var.set(self.controller.settings.warn)

        if self.warn_cbox_var.get():
            self.warn_entry.configure(state="normal")
            self.warn_entry.insert("0", str(self.controller.settings.warn_age))

        self.backup_entry.insert("0", str(self.controller.settings.saved_version_count))
        self.pass_gen_settings.set_values()

    def warn_entry_focus_out(self, event):
        if self.warn_entry.get():
            self.controller.passwords_controller.set_warn_age_setting(
                int(self.warn_entry.get())
            )

    def cbox_warn_com(self):
        if self.warn_cbox_var.get():
            self.warn_entry.configure(
                state="normal", placeholder_text="Days", fg_color="#ffffff"
            )
        else:
            self.warn_entry.configure(state="readonly", fg_color="#f2f2f2")
        self.controller.passwords_controller.set_warn_setting(self.warn_cbox_var.get())

    def on_close(self):
        # Release the grab when the window is closed
        self.controller.passwords_controller.set_saved_version_count_setting(
            int(self.backup_entry.get())
        )
        self.grab_release()
        self.destroy()


class PassGenWindow(ctk.CTkToplevel):
    def __init__(self, controller):
        ctk.CTkToplevel.__init__(self)
        self.title("Password Generator")
        self.set_geometry(400, 300)
        self.wait_visibility()
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.controller = controller
        # ---------- widgets ----------
        row_index = 0
        # check box settings
        self.pass_gen_settings = PassGenSettings(self, row_index)

        self.pass_entry = ctk.CTkEntry(self, width=300, state="readonly")
        self.pass_entry.place(anchor="c", relx=0.45, rely=0.7)
        self.pass_entropy = ctk.CTkLabel(self, text="0.0", text_color="red")
        self.pass_entropy.place(anchor="c", relx=0.9, rely=0.7)

        # actions button
        self.btn = ctk.CTkButton(
            master=self,
            width=150,
            height=30,
            text="Generate",
            font=("Trebuchet MS", 20, "bold"),
            command=self.btn_generate_com,
        )
        self.btn.place(anchor="c", relx=0.5, rely=0.9)
        # -----------------------------
        self.pass_gen_settings.set_values()

    def set_geometry(self, width, height):
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def btn_generate_com(self):
        self.pass_gen_settings.update_generate_pass_val()
        password = self.controller.passwords_controller.generate_password()
        self.pass_entry.configure(state="normal")
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert("0", password)
        self.pass_entry.configure(state="readonly")
        #! check password entropy

    def on_close(self):
        # Release the grab when the window is closed
        self.grab_release()
        self.destroy()


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
        self.wait_visibility()
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
        self.pass_trace = tk.StringVar()
        self.pass_trace.trace_add("write", lambda *args: self.update_entropy())
        self.pass_ent = self.ent_fields[1]
        self.pass_ent.configure(textvariable=self.pass_trace)
        self.entropy_label = ctk.CTkLabel(
            master=self, text="", fg_color="transparent", width=7
        )
        self.entropy_label.place(anchor="c", relx=0.96, rely=0.1035)
        self.update_entropy()
        self.gen_pass_btn = ctk.CTkButton(
            self, text="", width=20, height=20, command=self.btn_gen_pass_com
        )
        self.gen_pass_btn.place(anchor="c", relx=0.48, rely=0.1035)

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

    def update_entropy(self):
        entropy_bits = self.controller.passwords_controller.get_password_entropy(
            self.pass_trace.get()
        )

        # Define the minimum and maximum entropy bits
        min_entropy_bits = 0
        max_entropy_bits = 100
        normalized_entropy = min(entropy_bits, max_entropy_bits)
        # Normalize the entropy bits to a value between 0 and 1
        normalized_entropy = (normalized_entropy - min_entropy_bits) / (
            max_entropy_bits - min_entropy_bits
        )
        min_luminance = 20
        # Calculate the red and green values
        red = int((1 - normalized_entropy) * 255) + min_luminance
        red = red if red < 256 else 255
        green = int(normalized_entropy * 255) + min_luminance
        green = green if green < 256 else 255
        # Convert the color values to a hexadecimal string
        hex_color = "#{:02x}{:02x}{:02x}".format(red, green, min_luminance)
        self.entropy_label.configure(text=f"{entropy_bits:06.2f}", fg_color=hex_color)

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

    def btn_gen_pass_com(self):
        pass_gen = PassGenWindow(self.controller)

    def on_close(self):
        # Release the grab when the window is closed
        self.grab_release()
        self.destroy()


class PassMKFrame(ctk.CTkFrame):
    def __init__(self, controller):
        ctk.CTkFrame.__init__(self, controller.view_controller)

        self.controller = controller
        self.new_MK = True

        # ---------- widgets ----------
        # Entry for the password
        self.mk_pass = tk.StringVar()
        self.mk_pass.trace_add("write", lambda *args: self.update_entropy())
        self.mk_ent = ctk.CTkEntry(
            master=self,
            width=200,
            height=30,
            show="*",
            font=("Trebuchet MS", 15),
            placeholder_text="Master Key",
            textvariable=self.mk_pass,
        )
        self.mk_ent.place(anchor="c", relx=0.5, rely=0.4)

        self.entropy_label = ctk.CTkLabel(
            master=self, text="", fg_color="transparent", width=7
        )
        self.entropy_label.place(anchor="e", relx=0.5, rely=0.4, x=140)

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

    def update_entropy(self):
        if not self.new_MK:
            self.entropy_label.configure(text="", fg_color="transparent")
            return

        entropy_bits = self.controller.passwords_controller.get_password_entropy(
            self.mk_pass.get()
        )

        # Define the minimum and maximum entropy bits
        min_entropy_bits = 0
        max_entropy_bits = 100
        normalized_entropy = min(entropy_bits, max_entropy_bits)
        # Normalize the entropy bits to a value between 0 and 1
        normalized_entropy = (normalized_entropy - min_entropy_bits) / (
            max_entropy_bits - min_entropy_bits
        )
        min_luminance = 20
        # Calculate the red and green values
        red = int((1 - normalized_entropy) * 255) + min_luminance
        red = red if red < 256 else 255
        green = int(normalized_entropy * 255) + min_luminance
        green = green if green < 256 else 255
        # Convert the color values to a hexadecimal string
        hex_color = "#{:02x}{:02x}{:02x}".format(red, green, min_luminance)
        self.entropy_label.configure(text=f"{entropy_bits:06.2f}", fg_color=hex_color)

    def display(self, new_MK=True):
        self.focus_set()  # changing the focus from the entry when switching back to the same frame
        self.new_MK = new_MK
        self.update_entropy()
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
        self.mk_ent.delete(0, tk.END)

    def confirm_btn_com(self):
        if self.new_MK:
            self.controller.master_key = self.mk_ent.get()
            self.controller.save_path()
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
            self.controller.passwords_display_frame.display()
        else:
            result = self.controller.check_MK(self.mk_ent.get())
            if result:
                self.pop_up_window("File opened successfully!!", "green", "Success!")
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
                self.controller.passwords_display_frame.display()
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
        super().__init__(controller.view_controller)
        self.controller = controller
        self.frame = frame
        self.menubar = tk.Menu(
            controller.view_controller, font=("Trebuchet MS", 9, "bold")
        )
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
        self.tools_menu.add_command(
            label="Password Generator",
            command=self.pass_gen_clicked,
        )

        self.menubar.add_cascade(menu=self.file_menu, label="File")
        self.menubar.add_cascade(menu=self.tools_menu, label="Tools")
        self.menubar.add_cascade(label="Settings", command=self.settings_clicked)

    def display(self):
        self.controller.view_controller.config(menu=self.menubar)

    def new_file_clicked(self):
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Open", state="disabled"
        )
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "New", state="disabled"
        )
        self.controller.view_controller.config(menu="")
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

        self.controller.view_controller.config(menu="")
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
        # self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
        #     "Close", state="disabled"
        # )
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "Open", state="normal"
        )
        self.controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
            "New", state="normal"
        )
        self.controller.passwords_controller.close_file(save)
        self.controller.view_controller.config(menu="")
        self.controller.master_key = None
        self.controller.passwords_dec_data = []
        self.controller.passwords_file_path = None
        self.frame.pack_forget()
        self.controller.view_controller.init_frame.display()

    def settings_clicked(self):
        settings = SettingsWindow(self.controller)

    def pass_gen_clicked(self):
        pass_gen = PassGenWindow(self.controller)


class PasswordsDisplayFrame(ctk.CTkFrame):
    def __init__(self, controller):
        ctk.CTkFrame.__init__(self, controller.view_controller)

        self.pass_view_controller = controller
        self.menu_bar = PassMenuBar(self.pass_view_controller, self)

        # ---------- attributes ----------
        self.headers = ["ID", "Username", "password", "Tag", "URL"]
        self.hidden_headers = [
            "Notes",
            "password modification date",
            "Record modification date",
        ]

        self.headers_size = (10, 150, 180, 50, 250)
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

        # filter widgets -------------
        # filter entry 1
        self.username_fltr_ent = ctk.CTkEntry(
            self, width=100, placeholder_text="Username"
        )
        self.username_fltr_ent.place(anchor="c", relx=0.435, rely=0.05)
        # filter entry 2
        self.tag_fltr_ent = ctk.CTkEntry(self, width=100, placeholder_text="Tag")
        self.tag_fltr_ent.place(anchor="c", relx=0.585, rely=0.05)
        # filter entry 3
        self.url_fltr_ent = ctk.CTkEntry(self, width=100, placeholder_text="Url")
        self.url_fltr_ent.place(anchor="c", relx=0.735, rely=0.05)
        # ----------------------------

        # seach widgets -------------
        # search entry
        self.search_ent = ctk.CTkEntry(self, width=120, placeholder_text="search")
        self.search_ent.place(anchor="c", relx=0.885, rely=0.05)
        # search button
        self.search_btn = ctk.CTkButton(
            master=self,
            width=20,
            height=20,
            font=("Trebuchet MS", 15),
            text="⌕",
            command=self.filter_search_btn_com,
        )
        self.search_btn.place(anchor="c", relx=0.985, rely=0.05)
        # ---------------------------

        # data container
        self.data_tree = ttk.Treeview(self, columns=self.headers, show="headings")
        self.data_tree.pack(pady=0, fill="both", expand=True)

        # adding events to the data container
        self.data_tree.bind("<Double-1>", self.on_double_click_evt)
        self.data_tree.bind("<Button-1>", self.on_left_click_evt)
        self.data_tree.bind("<Button-3>", self.on_right_click_evt)
        self.add_btn.bind("<Button-1>", self.on_left_click_evt)
        self.bind("<Button-1>", self.on_left_click_evt)

        self.display_complete = tk.BooleanVar()

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
        self.display_complete.set(False)
        self.after(0, self.delay_display)
        while not self.display_complete.get():
            self.update()

    def delay_display(self):
        # Save current selection
        selected_ids = [
            self.data_tree.item(item)["values"][-1]
            for item in self.data_tree.selection()
        ]
        self.clear_data()
        self.fill_table(self.pass_view_controller.passwords_dec_data)
        if (
            not self.pass_view_controller.view_controller.init_frame.passwords_btn.winfo_ismapped()
            and not self.pass_view_controller.master_key_frame.confirm_btn.winfo_ismapped()
            and not self.pass_view_controller.view_controller.container_view.container_display_frame.add_btn.winfo_ismapped()
            and not self.pass_view_controller.view_controller.container_view.master_key_frame.confirm_btn.winfo_ismapped()
        ):
            self.pass_view_controller.passwords_display_frame.menu_bar.file_menu.entryconfig(
                "Close", state="normal"
            )
            if self.pass_view_controller.master_key:
                self.add_btn.configure(state="normal")
            else:
                self.add_btn.configure(state="disabled")
            self.menu_bar.display()
            self.pack(pady=10, padx=10, fill="both", expand=True)
            self.clear_data()
            self.fill_table(self.pass_view_controller.passwords_dec_data)

        # Reselect previously selected items
        for item in self.data_tree.get_children():
            if self.data_tree.item(item)["values"][-1] in selected_ids:
                self.data_tree.selection_add(item)

        self.display_complete.set(True)

    def fill_table(self, data):
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

            if row.warn:
                self.data_tree.insert("", "end", values=table_row, tags=("warn",))
            else:
                self.data_tree.insert("", "end", values=table_row)
            self.data_tree.tag_configure("warn", background="#F0ebd3")

    def clear_data(self):
        for item_id in self.data_tree.get_children():
            self.data_tree.delete(item_id)

    def on_double_click_evt(self, event):
        record_inter_id = self.data_tree.selection()[0]
        values = list(self.data_tree.item(record_inter_id, "values"))
        self.view_record(values, record_inter_id)

    def view_record(self, record_values, record_inter_id):
        record_window = RecordsWindow(
            self.pass_view_controller,
            self.data_tree,
            self.headers + self.hidden_headers,
        )
        record_window.view_record(record_values, record_inter_id)
        # for header, value in zip(self.headers, record_values):
        #     label = ctk.CTkLabel(record_window, text=f"{header}: {value}")
        #     label.pack()

    def on_left_click_evt(self, event):
        # Check if context_menu already exists and unpost it
        if hasattr(self, "context_menu"):
            self.context_menu.unpost()

    def on_right_click_evt(self, event):
        # Check if context_menu already exists and unpost it
        if hasattr(self, "context_menu"):
            self.context_menu.unpost()
        # Identify the item and column that were right-clicked
        record_inter_id = self.data_tree.identify_row(event.y)
        col_id = int(self.data_tree.identify_column(event.x).split("#")[1])
        if record_inter_id and col_id:
            record_values = self.data_tree.item(record_inter_id, "values")
            clicked_text = record_values[col_id - 1]

            self.context_menu = tk.Menu(self.data_tree, tearoff=0)
            self.context_menu.add_command(
                label="Copy", command=lambda: self.copy_text(clicked_text)
            )
            self.context_menu.add_command(
                label="Delete", command=lambda: self.delete_record(record_values[-1])
            )
            self.context_menu.post(event.x_root, event.y_root)

    def copy_text(self, text):
        self.data_tree.clipboard_clear()
        self.data_tree.clipboard_append(text)

    def delete_record(self, record_id):
        self.pass_view_controller.passwords_controller.delete_record(int(record_id))

    def add_btn_com(self):
        record_window = RecordsWindow(
            self.pass_view_controller,
            self.data_tree,
            self.headers + self.hidden_headers,
        )

    def filter_search_btn_com(self):
        self.pass_view_controller.filter_search(
            self.search_ent.get(),
            [
                self.username_fltr_ent.get(),
                self.tag_fltr_ent.get(),
                self.url_fltr_ent.get(),
            ],
        )


class PasswordsView:
    def __init__(self, view_controller):
        self.view_controller = view_controller
        self.passwords_controller = None

        # ---------- data ----------
        self.master_key = None
        self.passwords_file_path = None
        self.passwords_dec_data = []
        self.settings = None
        # --------------------------

        # ---------- frames ----------
        # master key window
        self.master_key_frame = PassMKFrame(self)
        # passwords
        self.passwords_display_frame = PasswordsDisplayFrame(self)
        # --------------------------------

    def pick_file(self):
        self.passwords_file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("All files", "*.pass*")],
            initialdir="./",
        )

    def save_path(self):
        self.passwords_file_path = filedialog.asksaveasfilename(
            title="Choose Destination",
            filetypes=[("All files", "*.pass*")],
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

    def view_passwords(self):
        self.passwords_display_frame.display()

    def update_data(self, new_data):
        self.passwords_dec_data = new_data
        self.passwords_display_frame.display()

    def update_settings(self, settings):
        self.settings = settings

    def filter_search(self, search_value, filter_values):
        self.passwords_controller.filter_search(filter_values, search_value)

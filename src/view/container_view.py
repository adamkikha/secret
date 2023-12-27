import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import filedialog
from src.utils import TimeOracle
from src.model.file_record import FileRecord


class AddRecordsWindow(ctk.CTkToplevel):
    """frame used to add a record"""

    def __init__(self, controller):
        ctk.CTkToplevel.__init__(self)

        self.title("View")
        self.set_geometry(500, 450)
        self.wait_visibility()
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.controller = controller
        self.headers = ["Filename", "Tag", "Notes"]
        self.file_path = None
        # ---------- widgets ----------

        self.file_path_label = ctk.CTkLabel(self, text=self.headers[0] + ":")
        self.file_path_label.grid(row=0, column=0, padx=50, pady=5, sticky="w")
        self.file_path_ent = ctk.CTkEntry(self, width=250, state="disabled")
        self.file_path_ent.grid(row=0, column=1, padx=5, pady=5)

        self.file_path_btn = ctk.CTkButton(
            self,
            width=40,
            height=20,
            text="pick",
            font=("Trebuchet MS", 15, "bold"),
            command=self.btn_file_path_com,
        )
        self.file_path_btn.place(anchor="c", relx=0.94, rely=0.04)

        self.tag_label = ctk.CTkLabel(self, text=self.headers[1] + ":")
        self.tag_label.grid(row=1, column=0, padx=50, pady=5, sticky="w")
        self.tag_ent = ctk.CTkEntry(self, width=250)
        self.tag_ent.grid(row=1, column=1, padx=5, pady=5)

        self.notes_label = ctk.CTkLabel(self, text=self.headers[2] + ":")
        self.notes_label.grid(row=4, column=0, padx=50, pady=5, sticky="w")

        # notes entry
        self.notes_ent = tk.Text(self, wrap="word", width=40, height=10)
        self.notes_ent.grid(row=4 + 1, column=1, padx=5, pady=5)

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

    def btn_file_path_com(self):
        self.file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("All files", "*.*")],
            initialdir="./",
        )
        self.file_path_ent.configure(state="normal")
        self.file_path_ent.insert(0, self.file_path)
        self.file_path_ent.configure(state="disabled")

    def btn_add_record_com(self):
        self.controller.add_file(
            self.file_path_ent.get(),
            self.tag_ent.get(),
            self.notes_ent.get("1.0", "end-1c"),
        )
        self.destroy()

    def on_close(self):
        # Release the grab when the window is closed
        self.grab_release()
        self.destroy()


class RecordsWindow(ctk.CTkToplevel):
    """frame used for add, view, and edit the records"""

    def __init__(self, controller, table_wid):
        """_summary_

        Args:
            table_wid (ttk.Treeview): table widget to update the view of the table
            headers (list): headers of the record
        """
        ctk.CTkToplevel.__init__(self)

        self.title("View")
        self.set_geometry(600, 550)
        self.wait_visibility()
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.ent_fields = []
        self.headers = ["Filename", "Tag", "Size", "Modification date", "Notes"]
        self.controller = controller
        self.data_table = table_wid
        self.record_id = None
        self.record_inter_id = None
        # ---------- widgets ----------

        self.file_name_label = ctk.CTkLabel(self, text=self.headers[0] + ":")
        self.file_name_label.grid(row=0, column=0, padx=50, pady=5, sticky="w")
        self.file_name_ent = ctk.CTkEntry(self, width=250)
        self.file_name_ent.grid(row=0, column=1, padx=5, pady=5)

        self.tag_label = ctk.CTkLabel(self, text=self.headers[1] + ":")
        self.tag_label.grid(row=1, column=0, padx=50, pady=5, sticky="w")
        self.tag_ent = ctk.CTkEntry(self, width=250)
        self.tag_ent.grid(row=1, column=1, padx=5, pady=5)

        self.size_label = ctk.CTkLabel(self, text=self.headers[2] + ":")
        self.size_label.grid(row=2, column=0, padx=50, pady=5, sticky="w")
        self.size_val = ctk.CTkLabel(self, width=250)
        self.size_val.grid(row=2, column=1, padx=5, pady=5)

        self.date_label = ctk.CTkLabel(self, text=self.headers[3] + ":")
        self.date_label.grid(row=3, column=0, padx=50, pady=5, sticky="w")
        self.date_val = ctk.CTkLabel(self, width=250)
        self.date_val.grid(row=3, column=1, padx=5, pady=5)

        self.notes_label = ctk.CTkLabel(self, text=self.headers[4] + ":")
        self.notes_label.grid(row=4, column=0, padx=50, pady=5, sticky="w")
        # notes entry
        self.notes_ent = tk.Text(self, wrap="word", width=40, height=10)
        self.notes_ent.grid(row=4 + 1, column=1, padx=5, pady=5)

        # actions button
        self.btn = ctk.CTkButton(
            master=self,
            width=150,
            height=30,
            text="Edit",
            font=("Trebuchet MS", 20, "bold"),
            command=self.btn_edit_com,
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

    def view_record(self, record, record_inter_id):
        """_summary_

        Args:
            record (list): "Filename", "Tag", "Notes", "Size", "Modification date", "ID"
            record_inter_id (int): the id of the record in the widget (used for GUI only)
        """
        self.record_id = record[-1]
        record.pop(0)  # get rid of the index
        record.pop()  # get rid of the id
        self.record_inter_id = record_inter_id

        self.file_name_ent.insert(0, record[0])

        self.tag_ent.insert(0, str(record[1]))
        self.tag_ent.configure(state="readonly", fg_color="#f2f2f2")

        self.notes_ent.insert("1.0", record[2])
        self.notes_ent.config(state="disabled", bg="#f2f2f2")

        self.size_val.configure(text=record[3])

        self.date_val.configure(text=record[4])

    def btn_edit_com(self):
        # make the fields editable
        self.tag_ent.configure(state="normal", fg_color="#ffffff")
        self.notes_ent.config(state="normal", bg="#ffffff")
        # change the button text and command function
        self.btn.configure(text="Confirm", command=self.btn_confirm_edit_com)

    def btn_confirm_edit_com(self):
        self.controller.edit_record(
            self.record_id,
            self.file_name_ent.get(),
            self.tag_ent.get(),
            self.notes_ent.get("1.0", "end-1c"),
        )
        self.destroy()

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

        entropy_bits = self.controller.container_controller.get_password_entropy(
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
        self.controller.container_display_frame.menu_bar.close_file_clicked(save=False)
        self.pack_forget()
        self.mk_ent.delete(0, tk.END)

    def confirm_btn_com(self):
        if self.new_MK:
            self.controller.master_key = self.mk_ent.get()
            self.controller.save_path()
            self.controller.container_display_frame.display()
            self.pop_up_window("Key set successfully!!", "green", "Success!")
            self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                "Lock", state="normal"
            )
            self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                "Close", state="normal"
            )
            self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                "Save", state="normal"
            )
            self.pack_forget()
        else:
            result = self.controller.check_MK(self.mk_ent.get())
            if result:
                self.pop_up_window(
                    "Container opened successfully!!", "green", "Success!"
                )
                self.controller.container_display_frame.display()
                self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                    "Lock", state="normal"
                )
                self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                    "Close", state="normal"
                )
                self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                    "Save", state="normal"
                )
                self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                    "Open", state="disabled"
                )
                self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                    "New", state="disabled"
                )
                self.pack_forget()
            else:
                self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                    "Open", state="normal"
                )
                self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
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


class ContMenuBar(tk.Menu):
    """
    Custom menubar for the container
    """

    def __init__(self, controller, frame):
        super().__init__(controller.view_controller)
        self.controller = controller
        self.frame = frame
        self.menubar = tk.Menu(
            controller.view_controller, font=("Trebuchet MS", 9, "bold")
        )
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label="New", command=self.new_file_clicked)
        self.file_menu.add_command(label="Open", command=self.open_file_clicked)
        self.file_menu.add_command(
            label="Save",
            state="disabled",
            command=self.save_file_clicked,
        )
        self.file_menu.add_command(
            label="Lock",
            state="disabled",
            command=self.lock_file_clicked,
        )

        self.file_menu.add_command(
            label="Close",
            state="disabled",
            command=self.close_file_clicked,
        )

        # self.settings_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(menu=self.file_menu, label="File")
        # self.menubar.add_cascade(menu=self.settings_menu, label="Settings")

    def display(self):
        self.controller.view_controller.config(menu=self.menubar)

    def new_file_clicked(self):
        self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "Open", state="disabled"
        )
        self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "New", state="disabled"
        )
        self.controller.view_controller.config(menu="")
        self.frame.pack_forget()
        self.controller.master_key_frame.display()

    def open_file_clicked(self):
        self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "Open", state="disabled"
        )
        self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "New", state="disabled"
        )
        if not self.controller.container_path:
            self.controller.pick_container()
            if not self.controller.container_path:  # user didn't pick file
                self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                    "Open", state="normal"
                )
                self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
                    "New", state="normal"
                )
                self.pack_forget()
                self.controller.container_display_frame.display()
                return

        self.controller.view_controller.config(menu="")
        self.frame.pack_forget()
        self.controller.master_key_frame.display(False)

    def save_file_clicked(self):
        self.controller.container_controller.save_file()

    def lock_file_clicked(self):
        self.controller.container_display_frame.filename_fltr_ent.delete(0, tk.END)
        self.controller.container_display_frame.sizel_fltr_ent.delete(0, tk.END)
        self.controller.container_display_frame.sizeu_fltr_ent.delete(0, tk.END)
        self.controller.container_display_frame.tag_ent.delete(0, tk.END)
        self.controller.container_display_frame.search_ent.delete(0, tk.END)
        self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "Lock", state="disabled"
        )

        self.controller.container_controller.close_file(save=True)

        self.controller.container_display_frame.pack_forget()
        self.controller.master_key = None
        self.controller.container_dec_data = []
        self.controller.master_key_frame.display(False)

    def close_file_clicked(self, save=True):
        self.controller.container_display_frame.filename_fltr_ent.delete(0, tk.END)
        self.controller.container_display_frame.sizel_fltr_ent.delete(0, tk.END)
        self.controller.container_display_frame.sizeu_fltr_ent.delete(0, tk.END)
        self.controller.container_display_frame.tag_ent.delete(0, tk.END)
        self.controller.container_display_frame.search_ent.delete(0, tk.END)
        self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "Lock", state="disabled"
        )
        self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "Save", state="disabled"
        )
        self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "Open", state="normal"
        )
        self.controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "New", state="normal"
        )
        self.controller.container_controller.close_file(save)
        self.controller.view_controller.config(menu="")
        self.controller.master_key = None
        self.controller.container_dec_data = []
        self.controller.container_path = None
        self.frame.pack_forget()
        self.controller.view_controller.init_frame.display()


class ContainersDisplayFrame(ctk.CTkFrame):
    def __init__(self, controller):
        ctk.CTkFrame.__init__(self, controller.view_controller)

        self.container_view_controller = controller

        self.menu_bar = ContMenuBar(self.container_view_controller, self)

        # ---------- attributes ----------
        self.headers = ["ID", "Filename", "Tag", "Notes", "Size", "Modification date"]

        self.headers_size = (10, 150, 50, 250, 50, 100)
        self.center_header_indeces = [0, 2, 4]

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
        self.filename_fltr_ent = ctk.CTkEntry(
            self, width=100, placeholder_text="Filename"
        )
        self.filename_fltr_ent.place(anchor="c", x=330, rely=0.05)
        # filter entry 2
        self.sizel_fltr_ent = ctk.CTkEntry(self, width=50, placeholder_text="from")
        self.sizel_fltr_ent.place(anchor="c", x=420, rely=0.05)
        # filter entry 3
        self.sizeu_fltr_ent = ctk.CTkEntry(self, width=50, placeholder_text="to")
        self.sizeu_fltr_ent.place(anchor="c", x=480, rely=0.05)
        # filter entry 4
        self.tag_ent = ctk.CTkEntry(self, width=100, placeholder_text="Tag")
        self.tag_ent.place(anchor="c", x=570, rely=0.05)

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
        self.fill_table(self.container_view_controller.container_dec_data)

        self.container_view_controller.container_display_frame.menu_bar.file_menu.entryconfig(
            "Close", state="normal"
        )
        if self.container_view_controller.master_key:
            self.add_btn.configure(state="normal")
        else:
            self.add_btn.configure(state="disabled")
        self.menu_bar.display()
        self.pack(pady=10, padx=10, fill="both", expand=True)
        self.clear_data()
        self.fill_table(self.container_view_controller.container_dec_data)

        # Reselect previously selected items
        for item in self.data_tree.get_children():
            if self.data_tree.item(item)["values"][-1] in selected_ids:
                self.data_tree.selection_add(item)

        self.display_complete.set(True)

    def fill_table(self, data: list[FileRecord]):
        for i, row in enumerate(data):
            table_row = [
                str(i + 1),
                row.name,
                row.tag,
                row.notes,
                str(row.size) + " bytes",
                TimeOracle.get_readable_time(row.record_mdate),
                row.id,
            ]
            self.data_tree.insert("", "end", values=table_row)

    def clear_data(self):
        for item_id in self.data_tree.get_children():
            self.data_tree.delete(item_id)

    def on_left_click_evt(self, event):
        # Check if context_menu already exists and unpost it
        if hasattr(self, "context_menu"):
            self.context_menu.unpost()

    def on_double_click_evt(self, event):
        # Check if context_menu already exists and unpost it
        if hasattr(self, "context_menu"):
            self.context_menu.unpost()
        record_inter_id = self.data_tree.selection()[0]
        values = list(self.data_tree.item(record_inter_id, "values"))
        self.view_record(values, record_inter_id)

    def view_record(self, record_values, record_inter_id):
        record_window = RecordsWindow(self.container_view_controller, self.data_tree)
        record_window.view_record(record_values, record_inter_id)

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
            context_menu.add_command(
                label="Export", command=lambda: self.export_record(record_values[-1])
            )

            context_menu.post(event.x_root, event.y_root)  # close the context_menu

    def copy_text(self, text):
        self.data_tree.clipboard_clear()
        self.data_tree.clipboard_append(text)

    def delete_record(self, record_id):
        self.container_view_controller.container_controller.delete_record(
            int(record_id)
        )

    def export_record(self, record_id):
        destination_path = filedialog.askdirectory(
            title="Choose Destination",
            initialdir="./",
        )
        self.container_view_controller.container_controller.export_decrypted_file(
            int(record_id), destination_path
        )

    def add_btn_com(self):
        record_window = AddRecordsWindow(self.container_view_controller)

    def filter_search_btn_com(self):
        self.container_view_controller.filter_search(
            self.search_ent.get(),
            [
                self.filename_fltr_ent.get(),
                self.sizel_fltr_ent.get(),
                self.sizeu_fltr_ent.get(),
                self.tag_ent.get(),
            ],
        )


class ContainerView:
    def __init__(self, view_controller):
        self.view_controller = view_controller

        self.container_controller = None

        # ---------- data ----------
        self.master_key = None
        self.container_path = None
        self.container_dec_data = []
        # --------------------------

        # ---------- frames ----------
        # master key window
        self.master_key_frame = PassMKFrame(self)
        # passwords
        self.container_display_frame = ContainersDisplayFrame(self)
        # --------------------------------

    def pick_container(self):
        # TODO: change the container type
        self.container_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("All files", "*.cont*")],
            initialdir="./",
        )

    def add_file(self, file_path: str, tag: str, notes: str):
        self.container_controller.add_file(file_path, tag, notes)

    def edit_record(self, id: int, name: str, tag: str, notes: str):
        self.container_controller.modify_record(int(id), name, tag, notes)

    def check_MK(self, master_key):
        self.master_key = master_key
        result = self.container_controller.open_file(master_key, self.container_path)
        return result

    def view_container(self):
        self.container_display_frame.display()

    def update_data(self, new_data: list[FileRecord]):
        self.container_dec_data = new_data
        self.container_display_frame.display()

    def save_path(self):
        self.container_path = filedialog.asksaveasfilename(
            title="Choose Destination",
            filetypes=[("All files", "*.cont*")],
            initialdir="./",
        )
        self.container_controller.create_file(self.master_key, self.container_path)

    def filter_search(self, search_value, filter_values):
        self.container_controller.filter_search(filter_values, search_value)

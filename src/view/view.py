import customtkinter as ctk
from src.view.passwords_view import PasswordsView
from src.view.container_view import ContainerView


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
            command=self.container_btn_function,
        )
        self.files_btn.place(anchor="c", relx=0.5, rely=0.5)
        # ---------------------------

    def display(self):
        self.pack(pady=10, padx=10, fill="both", expand=True)

    def passwords_btn_function(self):
        self.pack_forget()
        self.controller.passwords_view.view_passwords()

    def container_btn_function(self):
        self.pack_forget()
        self.controller.container_view.view_container()


class View(ctk.CTk):
    def __init__(self):
        super().__init__()

        # TODO: the following two lines should be moved to the setting window
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme(
            "dark-blue"
        )  # Themes: blue (default), dark-blue, green

        self.title("Secret")
        self.width = 800
        self.height = 700
        self.set_geometry()

        # ---------- frames ----------
        # initial window
        self.init_frame = InitFrame(self)
        # passwords
        self.passwords_view = PasswordsView(self)
        # files container
        self.container_view = ContainerView(self)
        # --------------------------------

        self.init_frame.display()

    def set_geometry(self):
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def set_passwords_controller(self, controller):
        self.passwords_view.passwords_controller = controller

    def set_container_controller(self, controller):
        self.container_view.container_controller = controller


if __name__ == "__main__":
    app = View()
    app.mainloop()

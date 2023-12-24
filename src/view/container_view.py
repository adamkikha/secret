from src.model.file_record import FileRecord


class ContainerView:
    def __init__(self, view_controller):
        self.view_controller = view_controller
        self.passwords_controller = None

        # ---------- data ----------
        self.master_key = None
        self.passwords_file_path = None
        self.passwords_dec_data = []
        # --------------------------

        # ---------- frames ----------
        # master key window
        # self.master_key_frame = PassMKFrame(self.view_controller)
        # passwords

        # --------------------------------

    def check_MK(self, master_key):
        pass

    def update_data(self, new_data: list[FileRecord]):
        pass






from src.controller.controller import Controller


class ContainerController(Controller):
    def set_container_model(self, model):
        self.model = model

    def add_file(self, file_path: str, tag: str, notes: str):
        self.model.add_file_record(file_path, tag, notes)

    def export_decrypted_file(self, id: int, destination_path: str):
        self.model.export_decrypted_file(id, destination_path)

    def modify_record(self, id: int, name: str, tag: str, notes: str):
        self.model.modify_file_record(id, name, tag, notes)

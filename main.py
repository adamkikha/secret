import threading
from src.utils import TimeOracle
from src.model.passwords_model import PasswordsModel
from src.model.container_model import ContainerModel
from src.controller.passwords_controller import PasswordsController
from src.controller.container_controller import ContainerController
from src.view.view import View


if __name__ == "__main__":
    time_oracle = TimeOracle()

    passwords_model = PasswordsModel(time_oracle)
    container_model = ContainerModel(time_oracle)

    time_oracle.set_model(passwords_model)

    passwords_controller = PasswordsController()
    container_controller = ContainerController()

    view = View()

    passwords_model.set_passwords_view(view.passwords_view)
    passwords_controller.set_passwords_model(passwords_model)
    view.set_passwords_controller(passwords_controller)

    container_model.set_container_view(view.container_view)
    container_controller.set_container_model(container_model)
    view.set_container_controller(container_controller)

    oracle_thread = threading.Thread(target=time_oracle.update_model, daemon=True)
    oracle_thread.start()

    view.mainloop()

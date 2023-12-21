from src.utils import TimeOracle
from src.model.passwords_model import PasswordsModel
from src.controller.passwords_controller import PasswordsController
from src.view.view import Secret


if __name__ == "__main__":
    time_oracle = TimeOracle()

    passwords_model = PasswordsModel(time_oracle)
    passwords_controller = PasswordsController()
    view = Secret()

    passwords_model.set_passwords_view(view.passwords_view)
    passwords_controller.set_passwords_model(passwords_model)
    view.set_passwords_controller(passwords_controller)

    view.mainloop()

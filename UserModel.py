from users import Users


class UserModel:

    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        if not Users.is_admin(telegram_id):
            self.role = 3
        elif Users.is_super_user(telegram_id):
            self.role = 1
        else:
            self.role = 2

    def change_role(self, super_user, role):
        Users.set_user_role(super_user, self.telegram_id, role)
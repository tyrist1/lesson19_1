from flask import current_app

from dao.model.user import UserSchema
from dao.user import UserDAO


class MovieService:
    def __init__(self, dao: UserDAO):
        self.dao = dao


class UsersService:
    def get_item_by_id(self, pk, ItemNotFound=None):
        user = UserDAO(self.session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        user = UserDAO(self.session).get_all()
        return UserSchema(many=True).dump(user)

    def get_item_by_email(self, email, ItemNotFound=None):
        user = UserDAO(self.session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_limit_users(self, page, ItemNotFound=None):
        limit = current_app.config["ITEMS_PER_PAGE"]
        offset = (page - 1) * limit
        users = UserDAO(self.session).get_limit(limit=limit, offset=offset)
        if not users:
            raise ItemNotFound
        return UserSchema(many=True).dump(users)

    def create(self, data_in):
        user_pass = data_in.get("password")
        if user_pass:
            data_in["password"] = generate_password_digest(user_pass)
            user = UserDAO(self.session).create(data_in)

        return UserSchema().dump(user)

    def update(self, data_in):
        user = UserDAO(self.session).update(data_in)
        return UserSchema().dump(user)

    def update_service(self, data_in, ItemNotFound=None):
        user_pass_1 = data_in.get("password_1")
        user_pass_2 = data_in.get("password_2")
        user = UserDAO(self.session).get_by_id(data_in.get("id"))
        if compare_passwords(user.password, user_pass_1):
            data_in["password"] = generate_password_digest(user_pass_2)
            user_upper = UserDAO(self._db_session).update(data_in)
            return UserSchema().dump(user_upper)
        else:
            raise ItemNotFound

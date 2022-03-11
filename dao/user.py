from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, pk):
        return self.session.query(User).filter(User.id == pk).one_or_none()

    def get_all(self):
        return self.session.query(User).all()

    def get_by_name(self, username):
        return self.session.query(User).filter(User.username == username).one_or_none()



    def create(self, data_in):
        obj = User(**data_in)
        self.session.add(obj)
        self.session.commit()
        return obj

    def update(self, data_in):
        obj = self.get_by_id(data_in.get('id'))
        if obj:
            if data_in.get('password'):
                obj.password = data_in.get('password')
            if data_in.get('username'):
                obj.username = data_in.get('username')
            self.session.add(obj)
            self.session.commit()
            return obj
        return "пользователь не обновлялся"

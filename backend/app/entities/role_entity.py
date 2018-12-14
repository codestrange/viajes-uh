class RoleEntity:
    def __init__(self, name, id=None, users=None, permissions=None):
        self.id = id
        self.name = name
        self.users = [] if users is None else users
        self.permissions = [] if permissions is None else permissions

    def to_json(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return f'<{self.name}>'

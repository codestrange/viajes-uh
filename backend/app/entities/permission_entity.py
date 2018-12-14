class PermissionEntity:
    def __init__(self, name, id=None, roles=None):
        self.id = id
        self.name = name
        self.roles = [] if roles is None else roles

    def to_json(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return f'<{self.name}>'

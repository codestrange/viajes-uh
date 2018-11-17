class Entity:
    @staticmethod
    def commit():
        raise NotImplementedError()

    @staticmethod
    def add(entity):
        raise NotImplementedError()

    @staticmethod
    def delete(entity):
        raise NotImplementedError()

    @staticmethod
    def query():
        raise NotImplementedError()

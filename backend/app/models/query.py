def query_decorator(f):
    def decorated_function(*args, **kwargs):
        return Query(f(*args, **kwargs))
    return decorated_function


class Query:
    def __init__(self, iterable, primary_key='id'):
        self.iterable = iterable
        self.primary_key = primary_key

    def all(self):
        return self.iterable

    def first(self):
        try:
            return next(self.iterable)
        except StopIteration:
            return None

    def get(self, identifier):
        for item in self.iterable:
            if item.__dict__[self.primary_key] == identifier:
                return item
        return None

    def count(self):
        return len(self.iterable)

    @query_decorator
    def filter(self, condition):
        return filter(condition, self.iterable)

    @query_decorator
    def limit(self, number):
        cont = 0
        for item in self.iterable:
            if cont < number:
                yield item
                cont += 1
            else:
                break

    @query_decorator
    def offset(self, number):
        cont = 0
        for item in self.iterable:
            if cont >= number:
                yield item
            else:
                cont += 1

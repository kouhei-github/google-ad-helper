
class Registry:
    def __init__(self):
        self._items = {}

    def set(self, key, value):
        self._items[key] = value

    def get(self, name):
        return self._items[name]


registry = Registry()

import lkml


class LookerView:
    def __init__(self, path):
        self.path = path
        self.view = self.load(path)

    @staticmethod
    def load(path):
        with open(path, "r") as file:
            result = lkml.load(file)
        return result

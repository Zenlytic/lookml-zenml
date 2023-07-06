import lkml


class LookerModel:
    def __init__(self, path):
        self.path = path
        self.model = self.load(path)

    @staticmethod
    def load(path):
        with open(path, "r") as file:
            result = lkml.load(file)
        return result

    def get_view_names(self):
        return [view["name"] for view in self.model["views"]]

    def get_view(self, view_name):
        for view in self.model["views"]:
            if view["name"] == view_name:
                return view
        return None

    def get_view_fields(self, view_name):
        view = self.get_view(view_name)
        return [field["name"] for field in view["fields"]]

    def get_view_field(self, view_name, field_name):
        view = self.get_view(view_name)
        for field in view["fields"]:
            if field["name"] == field_name:
                return field
        return None

    def add_view(self, view_name, view):
        self.model["views"].append(view)

    def add_view_field(self, view_name, field):
        view = self.get_view(view_name)
        view["fields"].append(field)

    def save(self):
        lkml.dump(self.model, open(self.path, "w"))

from pydrawio.mxgraphmodel import Object

class ComponentInfo:
    name: str
    component_type: str
    display_range: str
    description: str


    def __init__(self, obj: Object):
        try:
            self.name = obj.__dict__['name']
        except KeyError:
            self.name = ''

        try:
            self.component_type = obj.__dict__['type']
        except KeyError:
            self.component_type = ''

        try:
            self.display_range = obj.__dict__['display_range']
        except KeyError:
            self.display_range = ''

        try:
            self.description = obj.__dict__['description']
        except KeyError:
            self.description = ''

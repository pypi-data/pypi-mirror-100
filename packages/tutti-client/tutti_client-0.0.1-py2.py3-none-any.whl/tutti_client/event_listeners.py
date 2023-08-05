import ducts_client.event_listeners

class DuctEventListener(ducts_client.event_listeners.DuctEventListener):
    def __init__(self):
        super().__init__()
        self.handlers = {}

    def add_handler(self, event_name, handler):
        self.handlers[event_name].append(handler)

    def get_handlers(self, event_name):
        if event_name in self.handlers:
            return self.handlers[event_name]
        else:
            raise Exception(f"Event named '{event_name}' is not found")
        
    def on(self, names, handler):
        if isinstance(names, str):  names = [names]
        for name in names:  self.add_handler(name, handler)

class ResourceEventListener(DuctEventListener):
    def __init__(self):
        super().__init__()

        self.handlers = {
            "list_projects": [],
            "create_project": [],
        }

class MTurkEventListener(DuctEventListener):
    def __init__(self):
        super().__init__()

        self.handlers = {
        }

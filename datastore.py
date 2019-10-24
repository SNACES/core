class DataStore:
    def __init__(self):
        pass

    def create(self, name, items):
        raise NotImplementedError()

    def read(self, name, query):
        raise NotImplementedError()
        
    def update(self, name, items):
        raise NotImplementedError()
    
    def delete(self, name):
        raise NotImplementedError()
"""
Data Access Object interface compatible with any generic datastore 
used as an input for Process objects.
"""
class InputDAO:
    def read(self, query):
        raise NotImplementedError()
        
"""
Data Access Object interface compatible with any generic datastore 
used as an output for Process objects.
"""
class OutputDAO:
    def create(self, items):
        raise NotImplementedError()
    
    # def update(self, name, items):
    #     raise NotImplementedError()
    
    
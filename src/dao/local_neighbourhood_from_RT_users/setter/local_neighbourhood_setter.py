from src.model.local_neighbourhood import LocalNeighbourhood
from typing import Dict

class LocalNeighbourhoodSetter:
    def store_local_neighbourhood(self, local_neighbourhood: LocalNeighbourhood):
        raise NotImplementedError("Subclasses should implement this")

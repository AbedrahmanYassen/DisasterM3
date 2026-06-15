from abc import abstractmethod


class BaseDataset:
    def __init__(self):
        self.data = []

    def load(self):
        raise NotImplementedError
    @abstractmethod
    def _map_to_format(self):
        raise NotImplementedError
    

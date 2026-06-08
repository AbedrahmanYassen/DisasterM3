class BaseDataset:
    def __init__(self):
        self.data = []

    def load(self):
        raise NotImplementedError
    

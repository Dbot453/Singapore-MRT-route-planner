from abc import ABC, abstractmethod

class Ui(ABC):

    @abstractmethod
    def run(self):
        raise NotImplementedError
    
class Terminal:
    pass

class Gui:
    pass

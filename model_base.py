from abc import ABC, abstractmethod


class ModelBase(ABC):
    @abstractmethod
    def __init__(self, startingCash):
        pass

    @abstractmethod
    def calculateActions(self, indicators):
        pass

    @abstractmethod
    def accountHistory(self):
        pass

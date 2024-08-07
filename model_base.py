from abc import ABC, abstractmethod


class ModelBase(ABC):
    @abstractmethod
    def __init__(self, volumes):
        pass

    @abstractmethod
    def calculate_actions(self, indicators):
        pass

from abc import ABC, abstractmethod

class PhysicalSystem(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        if new_name.strip():
            self._name = new_name

    @abstractmethod
    def calculate_position(self, time: float) -> float:
        pass

    @abstractmethod
    def calculate_velocity(self, time: float) -> float:
        pass

    def __str__(self):
        return f"Sistema Físico: {self._name}"
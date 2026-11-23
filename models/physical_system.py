from abc import ABC, abstractmethod
from math import isfinite
from typing import TypeAlias

PhysicalValue: TypeAlias = float | tuple[float, ...]


class PhysicalSystem(ABC):
    def __init__(self, name: str):
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if not isinstance(new_name, str):
            raise TypeError("El nombre del sistema debe ser texto.")
        if not new_name.strip():
            raise ValueError("El nombre del sistema no puede estar vacío.")
        self._name = new_name.strip()

    @staticmethod
    def validate_parameter(
        name: str,
        value: float,
        minimum: float | None = None,
        *,
        strictly_greater: bool = False,
    ) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} debe ser un número.")
        try:
            finite = isfinite(value)
        except OverflowError:
            finite = False
        if not finite:
            raise ValueError(f"{name} debe ser un número finito.")
        if minimum is not None and (
            value <= minimum if strictly_greater else value < minimum
        ):
            relation = "mayor que" if strictly_greater else "mayor o igual que"
            raise ValueError(f"{name} debe ser {relation} {minimum}.")

    @staticmethod
    def validate_time(time: float) -> None:
        if isinstance(time, bool) or not isinstance(time, (int, float)):
            raise TypeError("El tiempo debe ser un número.")
        try:
            finite = isfinite(time)
        except OverflowError:
            finite = False
        if not finite or time < 0:
            raise ValueError("El tiempo debe ser un número finito no negativo.")

    @abstractmethod
    def calculate_position(self, time: float) -> PhysicalValue:
        raise NotImplementedError

    @abstractmethod
    def calculate_velocity(self, time: float) -> PhysicalValue:
        raise NotImplementedError

    @abstractmethod
    def calculate_acceleration(self, time: float) -> PhysicalValue:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"Sistema físico: {self.name}"

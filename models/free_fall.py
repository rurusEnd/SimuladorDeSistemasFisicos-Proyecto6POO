from math import sqrt

from models.physical_system import PhysicalSystem


class FreeFall(PhysicalSystem):
    def __init__(
        self, initial_height: float, gravity: float = 9.81, name: str = "Caída libre"
    ):
        super().__init__(name)
        self.validate_parameter("La altura inicial", initial_height, 0)
        self.validate_parameter("La gravedad", gravity, 0, strictly_greater=True)
        self._initial_height = initial_height
        self._gravity = gravity

    @property
    def initial_height(self) -> float:
        return self._initial_height

    @initial_height.setter
    def initial_height(self, value: float) -> None:
        self.validate_parameter("La altura inicial", value, 0)
        self._initial_height = value

    @property
    def gravity(self) -> float:
        return self._gravity

    def _impact_time(self) -> float:
        return sqrt(2 * self._initial_height / self._gravity)

    def calculate_position(self, time: float) -> float:
        self.validate_time(time)
        return max(0.0, self._initial_height - 0.5 * self._gravity * time**2)

    def calculate_velocity(self, time: float) -> float:
        self.validate_time(time)
        if time >= self._impact_time():
            return 0.0
        return -self._gravity * time

    def calculate_acceleration(self, time: float) -> float:
        self.validate_time(time)
        return 0.0 if time >= self._impact_time() else -self._gravity

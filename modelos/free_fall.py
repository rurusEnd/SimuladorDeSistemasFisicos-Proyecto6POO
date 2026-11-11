from models.physical_system import PhysicalSystem

class FreeFall(PhysicalSystem):
    def __init__(self, initial_height: float):
        super().__init__("Caída Libre")
        self._initial_height = initial_height
        self._gravity = 9.81

    @property
    def initial_height(self) -> float:
        return self._initial_height

    @initial_height.setter
    def initial_height(self, value: float):
        if value >= 0:
            self._initial_height = value

    def calculate_position(self, time: float) -> float:
        # y(t) = y0 - 0.5 * g * t^2
        position = self._initial_height - (0.5 * self._gravity * (time ** 2))
        return max(0.0, position)  # Evita atravesar el suelo

    def calculate_velocity(self, time: float) -> float:
        # v(t) = g * t
        return self._gravity * time
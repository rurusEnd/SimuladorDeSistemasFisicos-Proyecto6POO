from models.physical_system import PhysicalSystem

class LinearMotion(PhysicalSystem):
    def __init__(self, initial_position: float, initial_velocity: float, acceleration: float):
        super().__init__("Movimiento Rectilíneo (MRUV)")
        self._initial_position = initial_position
        self._initial_velocity = initial_velocity
        self._acceleration = acceleration

    @property
    def initial_position(self) -> float:
        return self._initial_position

    @property
    def initial_velocity(self) -> float:
        return self._initial_velocity

    @property
    def acceleration(self) -> float:
        return self._acceleration

    # Sobrescritura de métodos abstractos
    def calculate_position(self, time: float) -> float:
        # x(t) = x0 + v0*t + 0.5*a*t^2
        return self._initial_position + (self._initial_velocity * time) + (0.5 * self._acceleration * (time ** 2))

    def calculate_velocity(self, time: float) -> float:
        # v(t) = v0 + a*t
        return self._initial_velocity + (self._acceleration * time)
from models.physical_system import PhysicalSystem


class LinearMotion(PhysicalSystem):
    def __init__(
        self,
        initial_position: float,
        initial_velocity: float,
        acceleration: float,
        name: str = "Movimiento rectilíneo (MRUV)",
    ):
        super().__init__(name)
        self.validate_parameter("La posición inicial", initial_position)
        self.validate_parameter("La velocidad inicial", initial_velocity)
        self.validate_parameter("La aceleración", acceleration)
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

    def calculate_position(self, time: float) -> float:
        self.validate_time(time)
        # MRU is the a=0 case; MRUV uses x = x0 + v0*t + 1/2*a*t^2.
        return (
            self._initial_position
            + self._initial_velocity * time
            + 0.5 * self._acceleration * time**2
        )

    def calculate_velocity(self, time: float) -> float:
        self.validate_time(time)
        # Constant acceleration gives v = v0 + a*t.
        return self._initial_velocity + self._acceleration * time

    def calculate_acceleration(self, time: float) -> float:
        self.validate_time(time)
        return self._acceleration

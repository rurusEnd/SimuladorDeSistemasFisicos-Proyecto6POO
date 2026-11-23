from math import cos, radians, sin, sqrt

from models.physical_system import PhysicalSystem


class ProjectileMotion(PhysicalSystem):
    def __init__(
        self,
        initial_height: float,
        initial_speed: float,
        angle_degrees: float,
        gravity: float = 9.81,
        name: str = "Movimiento parabólico",
        *,
        initial_x: float = 0.0,
    ):
        super().__init__(name)
        self.validate_parameter("La altura inicial", initial_height, 0)
        self.validate_parameter("La rapidez inicial", initial_speed, 0)
        self.validate_parameter("El ángulo", angle_degrees)
        self.validate_parameter("La gravedad", gravity, 0, strictly_greater=True)
        self.validate_parameter("La posición horizontal inicial", initial_x)
        angle = radians(angle_degrees)
        self._initial_height = initial_height
        self._initial_x = initial_x
        self._velocity_x = initial_speed * cos(angle)
        self._velocity_y = initial_speed * sin(angle)
        self._gravity = gravity

    def _impact_time(self) -> float:
        if self._initial_height == 0 and self._velocity_y <= 0:
            return 0.0
        return (
            self._velocity_y
            + sqrt(self._velocity_y**2 + 2 * self._gravity * self._initial_height)
        ) / self._gravity

    def calculate_position(self, time: float) -> tuple[float, float]:
        self.validate_time(time)
        active_time = min(time, self._impact_time())
        x = self._initial_x + self._velocity_x * active_time
        y = max(
            0.0,
            self._initial_height
            + self._velocity_y * active_time
            - 0.5 * self._gravity * active_time**2,
        )
        return x, y

    def calculate_velocity(self, time: float) -> tuple[float, float]:
        self.validate_time(time)
        if time >= self._impact_time():
            return 0.0, 0.0
        return self._velocity_x, self._velocity_y - self._gravity * time

    def calculate_acceleration(self, time: float) -> tuple[float, float]:
        self.validate_time(time)
        if time >= self._impact_time():
            return 0.0, 0.0
        return 0.0, -self._gravity

from math import cos, degrees, radians, sin, sqrt

from models.physical_system import PhysicalSystem


class ProjectileMotion(PhysicalSystem):
    def __init__(
        self,
        initial_height: float,
        initial_speed: float,
        angle_degrees: float,
        gravity: float = 9.81,
        name: str = "Movimiento parabólico",
    ):
        super().__init__(name)
        self.validate_parameter("La altura inicial", initial_height, 0)
        self.validate_parameter("La rapidez inicial", initial_speed, 0)
        self.validate_parameter("El ángulo", angle_degrees)
        self.validate_parameter("La gravedad", gravity, 0, strictly_greater=True)
        self._initial_height = initial_height
        self._initial_x = 0.0
        self._initial_speed = initial_speed
        self._angle = radians(angle_degrees)
        self._gravity = gravity
        self._update_velocity_components()

    def _update_velocity_components(self) -> None:
        self._velocity_x = self._initial_speed * cos(self._angle)
        self._velocity_y = self._initial_speed * sin(self._angle)

    @property
    def initial_height(self) -> float:
        return self._initial_height

    @initial_height.setter
    def initial_height(self, value: float) -> None:
        self.validate_parameter("La altura inicial", value, 0)
        self._initial_height = value

    @property
    def initial_speed(self) -> float:
        return self._initial_speed

    @initial_speed.setter
    def initial_speed(self, value: float) -> None:
        self.validate_parameter("La rapidez inicial", value, 0)
        self._initial_speed = value
        self._update_velocity_components()

    @property
    def angle_degrees(self) -> float:
        return degrees(self._angle)

    @angle_degrees.setter
    def angle_degrees(self, value: float) -> None:
        self.validate_parameter("El ángulo", value)
        self._angle = radians(value)
        self._update_velocity_components()

    @property
    def gravity(self) -> float:
        return self._gravity

    @gravity.setter
    def gravity(self, value: float) -> None:
        self.validate_parameter("La gravedad", value, 0, strictly_greater=True)
        self._gravity = value

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

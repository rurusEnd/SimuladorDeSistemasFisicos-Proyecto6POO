from math import cos, radians, sin

from models.physical_system import PhysicalSystem


class CircularMotion(PhysicalSystem):
    def __init__(
        self,
        radius: float,
        angular_velocity: float,
        initial_angle_degrees: float = 0.0,
        name: str = "Movimiento circular",
    ):
        super().__init__(name)
        self.validate_parameter("El radio", radius, 0)
        self.validate_parameter("La velocidad angular", angular_velocity)
        self.validate_parameter("El ángulo inicial", initial_angle_degrees)
        self._radius = radius
        self._angular_velocity = angular_velocity
        self._initial_angle = radians(initial_angle_degrees)

    def _angle(self, time: float) -> float:
        return self._initial_angle + self._angular_velocity * time

    def calculate_position(self, time: float) -> tuple[float, float]:
        self.validate_time(time)
        angle = self._angle(time)
        return self._radius * cos(angle), self._radius * sin(angle)

    def calculate_velocity(self, time: float) -> tuple[float, float]:
        self.validate_time(time)
        angle = self._angle(time)
        return (
            -self._radius * self._angular_velocity * sin(angle),
            self._radius * self._angular_velocity * cos(angle),
        )

    def calculate_acceleration(self, time: float) -> tuple[float, float]:
        self.validate_time(time)
        angle = self._angle(time)
        centripetal_acceleration = self._radius * self._angular_velocity**2
        return (
            -centripetal_acceleration * cos(angle),
            -centripetal_acceleration * sin(angle),
        )
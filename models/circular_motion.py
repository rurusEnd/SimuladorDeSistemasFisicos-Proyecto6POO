from math import cos, radians, sin

from models.physical_system import PhysicalSystem


class CircularMotion(PhysicalSystem):
    def __init__(
        self,
        radius: float,
        angular_velocity: float,
        initial_angle_degrees: float = 0.0,
        name: str = "Movimiento circular",
        *,
        center_x: float = 0.0,
        center_y: float = 0.0,
        angular_acceleration: float = 0.0,
    ):
        super().__init__(name)
        self.validate_parameter("El radio", radius, 0, strictly_greater=True)
        self.validate_parameter("La velocidad angular", angular_velocity)
        self.validate_parameter("El ángulo inicial", initial_angle_degrees)
        self.validate_parameter("La coordenada x del centro", center_x)
        self.validate_parameter("La coordenada y del centro", center_y)
        self.validate_parameter("La aceleración angular", angular_acceleration)
        self._radius = radius
        self._angular_velocity = angular_velocity
        self._initial_angle = radians(initial_angle_degrees)
        self._center_x = center_x
        self._center_y = center_y
        self._angular_acceleration = angular_acceleration

    def _angle(self, time: float) -> float:
        return (
            self._initial_angle
            + self._angular_velocity * time
            + 0.5 * self._angular_acceleration * time**2
        )

    def _angular_velocity_at(self, time: float) -> float:
        return self._angular_velocity + self._angular_acceleration * time

    def calculate_position(self, time: float) -> tuple[float, float]:
        self.validate_time(time)
        angle = self._angle(time)
        return (
            self._center_x + self._radius * cos(angle),
            self._center_y + self._radius * sin(angle),
        )

    def calculate_velocity(self, time: float) -> tuple[float, float]:
        self.validate_time(time)
        angle = self._angle(time)
        angular_velocity = self._angular_velocity_at(time)
        return (
            -self._radius * angular_velocity * sin(angle),
            self._radius * angular_velocity * cos(angle),
        )

    def calculate_acceleration(self, time: float) -> tuple[float, float]:
        self.validate_time(time)
        angle = self._angle(time)
        angular_velocity = self._angular_velocity_at(time)
        return (
            -self._radius
            * (
                self._angular_acceleration * sin(angle)
                + angular_velocity**2 * cos(angle)
            ),
            self._radius
            * (
                self._angular_acceleration * cos(angle)
                - angular_velocity**2 * sin(angle)
            ),
        )
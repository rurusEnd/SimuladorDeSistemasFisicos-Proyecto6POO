from math import cos, radians, sin

from models.physical_system import PhysicalSystem


class Oscillator(PhysicalSystem):
    def __init__(
        self,
        amplitude: float,
        angular_frequency: float,
        phase_degrees: float = 0.0,
        name: str = "Oscilador armónico",
    ):
        super().__init__(name)
        self.validate_parameter("La amplitud", amplitude, 0)
        self.validate_parameter(
            "La frecuencia angular", angular_frequency, 0, strictly_greater=True
        )
        self.validate_parameter("La fase", phase_degrees)
        self._amplitude = amplitude
        self._angular_frequency = angular_frequency
        self._phase = radians(phase_degrees)

    def _angle(self, time: float) -> float:
        return self._angular_frequency * time + self._phase

    def calculate_position(self, time: float) -> float:
        self.validate_time(time)
        return self._amplitude * cos(self._angle(time))

    def calculate_velocity(self, time: float) -> float:
        self.validate_time(time)
        return -self._amplitude * self._angular_frequency * sin(self._angle(time))

    def calculate_acceleration(self, time: float) -> float:
        self.validate_time(time)
        return -self._angular_frequency**2 * self.calculate_position(time)

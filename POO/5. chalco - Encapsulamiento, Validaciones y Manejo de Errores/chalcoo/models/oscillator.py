from math import cos, degrees, radians, sin

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

    @property
    def amplitude(self) -> float:
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value: float) -> None:
        self.validate_parameter("La amplitud", value, 0)
        self._amplitude = value

    @property
    def angular_frequency(self) -> float:
        return self._angular_frequency

    @angular_frequency.setter
    def angular_frequency(self, value: float) -> None:
        self.validate_parameter(
            "La frecuencia angular", value, 0, strictly_greater=True
        )
        self._angular_frequency = value

    @property
    def phase_degrees(self) -> float:
        return degrees(self._phase)

    @phase_degrees.setter
    def phase_degrees(self, value: float) -> None:
        self.validate_parameter("La fase", value)
        self._phase = radians(value)

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

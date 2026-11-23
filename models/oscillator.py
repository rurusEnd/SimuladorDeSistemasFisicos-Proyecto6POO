from math import cos, radians, sin, sqrt

from models.physical_system import PhysicalSystem


class Oscillator(PhysicalSystem):
    def __init__(
        self,
        amplitude: float,
        angular_frequency: float | None = None,
        phase_degrees: float = 0.0,
        name: str = "Oscilador armónico",
        *,
        mass: float | None = None,
        spring_constant: float | None = None,
    ):
        super().__init__(name)
        self.validate_parameter("La amplitud", amplitude, 0)
        self.validate_parameter("La fase", phase_degrees)

        if (mass is None) != (spring_constant is None):
            raise ValueError(
                "Para calcular la frecuencia natural, indique masa y "
                "constante del resorte."
            )
        if mass is not None and spring_constant is not None:
            if angular_frequency is not None:
                raise ValueError(
                    "Indique la frecuencia angular o masa y constante del resorte, "
                    "no ambos."
                )
            self.validate_parameter("La masa", mass, 0, strictly_greater=True)
            self.validate_parameter(
                "La constante del resorte",
                spring_constant,
                0,
                strictly_greater=True,
            )
            angular_frequency = sqrt(spring_constant / mass)
        elif angular_frequency is None:
            raise ValueError(
                "Indique la frecuencia angular o masa y constante del resorte."
            )

        self.validate_parameter(
            "La frecuencia angular",
            angular_frequency,
            0,
            strictly_greater=True,
        )
        self._amplitude = amplitude
        self._angular_frequency = angular_frequency
        self._phase = radians(phase_degrees)
        self._mass = mass
        self._spring_constant = spring_constant

    @property
    def angular_frequency(self) -> float:
        return self._angular_frequency

    @property
    def mass(self) -> float | None:
        return self._mass

    @property
    def spring_constant(self) -> float | None:
        return self._spring_constant

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

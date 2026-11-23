import csv
import json
from dataclasses import dataclass
from math import ceil, hypot, isfinite
from pathlib import Path

from models.physical_system import PhysicalSystem, PhysicalValue

MAX_SAMPLES = 100_000


def _format_value(value: PhysicalValue) -> str:
    if isinstance(value, tuple):
        return "(" + ", ".join(f"{component:.3f}" for component in value) + ")"
    return f"{value:.3f}"


def _magnitude(value: PhysicalValue) -> float:
    if isinstance(value, tuple):
        return hypot(*value) if len(value) == 2 else sum(
            component**2 for component in value
        ) ** 0.5
    return abs(value)


def _csv_value(value: PhysicalValue) -> str:
    return json.dumps(value, ensure_ascii=False)


@dataclass(frozen=True)
class Result:
    time: float
    position: PhysicalValue
    velocity: PhysicalValue
    acceleration: PhysicalValue

    def __str__(self) -> str:
        return (
            f"[t={self.time:.3f} s] "
            f"Posición: {_format_value(self.position)}, "
            f"velocidad: {_format_value(self.velocity)}, "
            f"aceleración: {_format_value(self.acceleration)}"
        )


class Simulation:
    def __init__(self, name: str):
        self.name = name
        self.systems: list[PhysicalSystem] = []
        self.history: dict[str, list[Result]] = {}
        self._system_names: dict[PhysicalSystem, str] = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("El nombre de la simulación debe ser texto.")
        if not value.strip():
            raise ValueError("El nombre de la simulación no puede estar vacío.")
        self._name = value.strip()

    def add_system(self, system: PhysicalSystem, name: str | None = None) -> str:
        if not isinstance(system, PhysicalSystem):
            raise TypeError("El sistema debe ser una instancia de PhysicalSystem.")
        if system in self.systems:
            raise ValueError("El sistema ya está registrado en esta simulación.")

        if name is not None and not isinstance(name, str):
            raise TypeError("El nombre del sistema debe ser texto.")
        base_name = name.strip() if name is not None else system.name
        if not base_name:
            raise ValueError("El nombre del sistema no puede estar vacío.")

        unique_name = base_name
        suffix = 2
        while unique_name in self.history:
            unique_name = f"{base_name} ({suffix})"
            suffix += 1

        system.name = unique_name
        self.systems.append(system)
        self.history[unique_name] = []
        self._system_names[system] = unique_name
        return unique_name

    def run_all(self, time: float) -> dict[str, Result]:
        if not self.systems:
            raise ValueError("Agregue al menos un sistema antes de simular.")
        for system in self.systems:
            system.validate_time(time)

        results: dict[str, Result] = {}
        for system in self.systems:
            position = system.calculate_position(time)
            velocity = system.calculate_velocity(time)
            acceleration = system.calculate_acceleration(time)
            for label, value in (
                ("posición", position),
                ("velocidad", velocity),
                ("aceleración", acceleration),
            ):
                values = value if isinstance(value, tuple) else (value,)
                if not all(isfinite(component) for component in values):
                    raise ValueError(
                        f"El sistema '{self._system_names[system]}' produjo "
                        f"un valor no finito para {label}."
                    )

            result = Result(
                time=time,
                position=position,
                velocity=velocity,
                acceleration=acceleration,
            )
            results[self._system_names[system]] = result

        for name, result in results.items():
            self.history[name].append(result)
        return results

    def simulate(self, duration: float, time_step: float) -> int:
        PhysicalSystem.validate_parameter("La duración", duration, 0)
        PhysicalSystem.validate_parameter(
            "El intervalo", time_step, 0, strictly_greater=True
        )
        ratio = duration / time_step
        if not isfinite(ratio) or ratio > MAX_SAMPLES - 1:
            raise ValueError(
                f"La simulación excede el máximo de {MAX_SAMPLES:,} muestras."
            )
        sample_count = ceil(ratio) + 1

        for index in range(sample_count):
            time = min(index * time_step, duration)
            self.run_all(time)
        return sample_count

    def latest_results(self) -> dict[str, Result]:
        return {
            name: results[-1]
            for name, results in self.history.items()
            if results
        }

    def save_csv(self, file_path: str | Path) -> Path:
        if not any(self.history.values()):
            raise ValueError("No hay resultados para guardar.")

        path = Path(file_path)
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["sistema", "tiempo_s", "posición", "velocidad", "aceleración"]
            )
            for name, results in self.history.items():
                for result in results:
                    writer.writerow(
                        [
                            name,
                            result.time,
                            _csv_value(result.position),
                            _csv_value(result.velocity),
                            _csv_value(result.acceleration),
                        ]
                    )
        return path

    def show_summary(self) -> None:
        print(f"\n=== REPORTE DE SIMULACIÓN: {self.name} ===")
        for system_name, results in self.history.items():
            print(f"\n-> Sistema: {system_name}")
            for result in results:
                print(f"   {result}")

    def show_comparison(self) -> None:
        latest = self.latest_results()
        if not latest:
            print("Todavía no hay resultados para comparar.")
            return

        print("\n=== COMPARACIÓN EN EL ÚLTIMO INSTANTE SIMULADO ===")
        print(
            f"{'Sistema':<30} {'Posición':<24} "
            f"{'|Velocidad|':>14} {'|Aceleración|':>16}"
        )
        for name, result in latest.items():
            print(
                f"{name:<30} "
                f"{_format_value(result.position):<24} "
                f"{_magnitude(result.velocity):>14.3f} "
                f"{_magnitude(result.acceleration):>16.3f}"
            )

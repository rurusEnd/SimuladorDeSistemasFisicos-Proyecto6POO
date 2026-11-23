from math import isfinite

from models.circular_motion import CircularMotion
from models.free_fall import FreeFall
from models.linear_motion import LinearMotion
from models.oscillator import Oscillator
from models.projectile import ProjectileMotion
from models.physical_system import PhysicalSystem
from models.simulation import Simulation


def read_float(
    prompt: str,
    minimum: float | None = None,
    *,
    strictly_greater: bool = False,
    default: float | None = None,
) -> float:
    while True:
        raw_value = input(prompt).strip()
        if not raw_value and default is not None:
            return default
        try:
            value = float(raw_value)
        except ValueError:
            print("Ingrese un número válido.")
            continue

        valid = isfinite(value)
        if minimum is not None:
            valid = valid and (
                value > minimum if strictly_greater else value >= minimum
            )
        if valid:
            return value

        if minimum is None:
            print("El valor debe ser un número finito.")
        else:
            relation = "mayor que" if strictly_greater else "mayor o igual que"
            print(f"El valor debe ser {relation} {minimum}.")


def create_system() -> PhysicalSystem:
    print(
        "\nTipos de sistema:"
        "\n1. Movimiento rectilíneo (MRUV)"
        "\n2. Caída libre"
        "\n3. Movimiento parabólico"
        "\n4. Movimiento circular"
        "\n5. Oscilador armónico"
    )
    while True:
        choice = input("Seleccione el tipo: ").strip()
        if choice in {"1", "2", "3", "4", "5"}:
            break
        print("Seleccione una opción del 1 al 5.")

    if choice == "1":
        system = LinearMotion(
            read_float("Posición inicial (m): "),
            read_float("Velocidad inicial (m/s): "),
            read_float("Aceleración (m/s²): "),
        )
    elif choice == "2":
        system = FreeFall(
            read_float("Altura inicial (m): ", 0),
            read_float("Gravedad (m/s²) [9.81]: ", default=9.81),
        )
    elif choice == "3":
        system = ProjectileMotion(
            initial_height=read_float("Altura inicial y0 (m): ", 0),
            initial_speed=read_float("Rapidez inicial v0 (m/s): ", 0),
            angle_degrees=read_float(
                "Ángulo respecto a la horizontal (grados): "
            ),
            gravity=read_float("Gravedad (m/s²) [9.81]: ", default=9.81),
            initial_x=read_float("Posición horizontal inicial x0 (m) [0]: ", default=0),
        )
    elif choice == "4":
        system = CircularMotion(
            radius=read_float("Radio (m): ", 0, strictly_greater=True),
            angular_velocity=read_float("Velocidad angular inicial (rad/s): "),
            initial_angle_degrees=read_float(
                "Ángulo inicial (grados) [0]: ", default=0
            ),
            center_x=read_float("Coordenada x del centro (m) [0]: ", default=0),
            center_y=read_float("Coordenada y del centro (m) [0]: ", default=0),
            angular_acceleration=read_float(
                "Aceleración angular (rad/s²) [0]: ", default=0
            ),
        )
    else:
        amplitude = read_float("Amplitud (m): ", 0)
        use_spring = input(
            "¿Calcular frecuencia con masa y constante del resorte? (s/N): "
        ).strip().lower() == "s"
        phase = read_float("Fase inicial (grados) [0]: ", default=0)
        if use_spring:
            mass = read_float("Masa (kg): ", 0, strictly_greater=True)
            spring_constant = read_float(
                "Constante del resorte (N/m): ", 0, strictly_greater=True
            )
            system = Oscillator(
                amplitude=amplitude,
                phase_degrees=phase,
                mass=mass,
                spring_constant=spring_constant,
            )
        else:
            system = Oscillator(
                amplitude=amplitude,
                angular_frequency=read_float(
                    "Frecuencia angular (rad/s): ", 0, strictly_greater=True
                ),
                phase_degrees=phase,
            )

    name = input(f"Nombre del sistema [{system.name}]: ").strip()
    if name:
        system.name = name
    return system


def main() -> None:
    simulation = Simulation("Simulador de sistemas físicos")
    simulation.add_system(FreeFall(initial_height=100.0))
    simulation.add_system(
        LinearMotion(initial_position=0.0, initial_velocity=5.0, acceleration=2.0)
    )

    print("=== SIMULADOR DE SISTEMAS FÍSICOS ===")
    while True:
        print(
            "\n1. Agregar sistema"
            "\n2. Ejecutar simulación"
            "\n3. Comparar resultados"
            "\n4. Guardar resultados en CSV"
            "\n5. Ver historial completo"
            "\n6. Salir"
        )
        choice = input("Opción: ").strip()

        if choice == "1":
            system = create_system()
            name = simulation.add_system(system)
            print(f"Sistema '{name}' agregado.")
        elif choice == "2":
            duration = read_float("Duración total (s): ", 0)
            time_step = read_float(
                "Intervalo entre muestras (s): ", 0, strictly_greater=True
            )
            try:
                count = simulation.simulate(duration, time_step)
            except (ValueError, ArithmeticError) as error:
                print(f"No se pudo ejecutar la simulación: {error}")
                continue
            print(f"Simulación completada: {count} instantes calculados.")
            simulation.show_comparison()
        elif choice == "3":
            simulation.show_comparison()
        elif choice == "4":
            file_path = input("Archivo CSV [resultados.csv]: ").strip()
            try:
                saved_path = simulation.save_csv(file_path or "resultados.csv")
            except (OSError, ValueError) as error:
                print(f"No se pudieron guardar los resultados: {error}")
                continue
            print(f"Resultados guardados en: {saved_path.resolve()}")
        elif choice == "5":
            simulation.show_summary()
        elif choice == "6":
            print("Simulador finalizado.")
            break
        else:
            print("Opción inválida. Elija una opción del 1 al 6.")


if __name__ == "__main__":
    main()

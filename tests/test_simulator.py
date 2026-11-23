import csv
import io
import math
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from main import create_system, main
from models.circular_motion import CircularMotion
from models.free_fall import FreeFall
from models.linear_motion import LinearMotion
from models.oscillator import Oscillator
from models.projectile import ProjectileMotion
from models.simulation import Simulation


class PhysicalSystemTests(unittest.TestCase):
    def test_linear_motion_calculates_position_velocity_and_acceleration(self):
        system = LinearMotion(initial_position=2, initial_velocity=3, acceleration=4)

        self.assertEqual(system.calculate_position(2), 16)
        self.assertEqual(system.calculate_velocity(2), 11)
        self.assertEqual(system.calculate_acceleration(2), 4)

    def test_free_fall_stops_at_ground(self):
        system = FreeFall(initial_height=4)

        self.assertAlmostEqual(system.calculate_position(0.5), 2.77375)
        self.assertEqual(system.calculate_velocity(1), 0)
        self.assertEqual(system.calculate_acceleration(1), 0)

    def test_projectile_calculates_two_dimensional_motion_and_impact(self):
        system = ProjectileMotion(
            initial_height=10, initial_speed=10, angle_degrees=30, initial_x=4
        )
        x, y = system.calculate_position(1)

        self.assertAlmostEqual(x, 4 + 10 * math.cos(math.radians(30)))
        self.assertAlmostEqual(y, 10 + 5 - 0.5 * 9.81)
        self.assertEqual(system.calculate_acceleration(100), (0, 0))

    def test_circular_motion_has_centripetal_acceleration(self):
        system = CircularMotion(
            radius=2,
            angular_velocity=3,
            center_x=1,
            center_y=-1,
            angular_acceleration=4,
        )

        self.assertEqual(system.calculate_position(0), (3, -1))
        self.assertEqual(system.calculate_velocity(0), (0, 6))
        self.assertEqual(system.calculate_acceleration(0), (-18, 8))

    def test_oscillator_calculates_simple_harmonic_motion(self):
        system = Oscillator(amplitude=2, mass=2, spring_constant=8)

        self.assertEqual(system.angular_frequency, 2)
        self.assertEqual(system.mass, 2)
        self.assertEqual(system.spring_constant, 8)
        self.assertEqual(system.calculate_position(0), 2)
        self.assertEqual(system.calculate_velocity(0), 0)
        self.assertEqual(system.calculate_acceleration(0), -8)

    def test_oscillator_rejects_incomplete_mass_spring_parameters(self):
        with self.assertRaises(ValueError):
            Oscillator(amplitude=2, mass=2)

    def test_system_rejects_invalid_time_and_parameters(self):
        system = LinearMotion(0, 1, 0)

        with self.assertRaises(ValueError):
            system.calculate_position(-1)
        with self.assertRaises(ValueError):
            FreeFall(initial_height=-1)

    def test_numeric_inputs_reject_non_numbers_and_booleans(self):
        with self.assertRaises(TypeError):
            LinearMotion(initial_position=0, initial_velocity="3", acceleration=0)
        with self.assertRaises(TypeError):
            LinearMotion(initial_position=False, initial_velocity=3, acceleration=0)

        system = LinearMotion(0, 1, 0)
        with self.assertRaises(TypeError):
            system.calculate_position("2")

    def test_model_properties_validate_and_update_parameters(self):
        linear = LinearMotion(0, 1, 0)
        linear.initial_position = 2
        linear.initial_velocity = 3
        linear.acceleration = 4
        self.assertEqual(linear.calculate_position(2), 16)
        with self.assertRaises(TypeError):
            linear.acceleration = "4"
        self.assertEqual(linear.acceleration, 4)

        free_fall = FreeFall(initial_height=4)
        with self.assertRaises(ValueError):
            free_fall.gravity = 0
        self.assertEqual(free_fall.gravity, 9.81)

        projectile = ProjectileMotion(0, 2, 0)
        projectile.initial_speed = 4
        projectile.angle_degrees = 90
        self.assertAlmostEqual(projectile.calculate_velocity(0)[1], 4)

        circular = CircularMotion(radius=2, angular_velocity=1)
        circular.radius = 3
        circular.center_x = 5
        self.assertEqual(circular.calculate_position(0), (8, 0))

        oscillator = Oscillator(amplitude=2, mass=2, spring_constant=8)
        oscillator.mass = 8
        self.assertEqual(oscillator.angular_frequency, 1)


class SimulationTests(unittest.TestCase):
    def test_simulation_includes_start_and_exact_end_times(self):
        simulation = Simulation("prueba")
        simulation.add_system(LinearMotion(0, 1, 0))

        sample_count = simulation.simulate(duration=1, time_step=0.3)

        self.assertEqual(sample_count, 5)
        times = [
            result.time
            for result in simulation.history["Movimiento rectilíneo (MRUV)"]
        ]
        for actual, expected in zip(times, [0, 0.3, 0.6, 0.9, 1]):
            self.assertAlmostEqual(actual, expected)

    def test_simulation_unique_names_and_comparison_results(self):
        simulation = Simulation("prueba")
        first = simulation.add_system(LinearMotion(0, 1, 0), name="Prueba")
        second = simulation.add_system(LinearMotion(0, 2, 0), name="Prueba")

        simulation.run_all(2)

        self.assertEqual((first, second), ("Prueba", "Prueba (2)"))
        self.assertEqual(simulation.latest_results()["Prueba"].position, 2)
        self.assertEqual(simulation.latest_results()["Prueba (2)"].position, 4)

    def test_simulation_saves_all_samples_to_csv(self):
        simulation = Simulation("prueba")
        simulation.add_system(LinearMotion(0, 1, 0))
        simulation.simulate(duration=1, time_step=0.5)

        with tempfile.TemporaryDirectory() as directory:
            path = simulation.save_csv(Path(directory) / "results.csv")
            with path.open(newline="", encoding="utf-8") as file:
                rows = list(csv.reader(file))

        self.assertEqual(
            rows[0],
            ["sistema", "tiempo_s", "posición", "velocidad", "aceleración"],
        )
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[-1][1], "1.0")

    def test_simulation_rejects_empty_system_list_and_invalid_step(self):
        simulation = Simulation("prueba")

        with self.assertRaises(ValueError):
            simulation.simulate(1, 0.1)

        simulation.add_system(LinearMotion(0, 1, 0))
        with self.assertRaises(ValueError):
            simulation.simulate(1, 0)

    def test_simulation_validates_name_and_system_types(self):
        with self.assertRaises(TypeError):
            Simulation(123)

        simulation = Simulation("prueba")
        with self.assertRaises(TypeError):
            simulation.add_system("sistema")
        with self.assertRaises(TypeError):
            simulation.add_system(LinearMotion(0, 1, 0), name=1)

    def test_simulation_rejects_too_many_samples(self):
        simulation = Simulation("prueba")
        simulation.add_system(LinearMotion(0, 1, 0))

        with self.assertRaises(ValueError):
            simulation.simulate(duration=100_000, time_step=1)

    def test_failed_sample_does_not_partially_update_history(self):
        simulation = Simulation("prueba")
        simulation.add_system(LinearMotion(0, 0, 0), name="estable")
        simulation.add_system(LinearMotion(0, 1e308, 0), name="desborde")

        with self.assertRaises(ValueError):
            simulation.simulate(duration=10, time_step=10)

        self.assertEqual(len(simulation.history["estable"]), 1)
        self.assertEqual(len(simulation.history["desborde"]), 1)


class MenuTests(unittest.TestCase):
    def test_menu_builds_spring_oscillator_from_teammate_parameters(self):
        responses = ["5", "2", "s", "0", "2", "8", ""]
        with patch("builtins.input", side_effect=responses):
            system = create_system()

        self.assertIsInstance(system, Oscillator)
        self.assertEqual(system.angular_frequency, 2)

    def test_menu_can_run_simulation_show_history_and_exit(self):
        responses = ["2", "0", "0.1", "5", "6"]
        output = io.StringIO()

        with patch("builtins.input", side_effect=responses), redirect_stdout(output):
            main()

        self.assertIn("Simulación completada: 1 instantes calculados.", output.getvalue())
        self.assertIn("REPORTE DE SIMULACIÓN", output.getvalue())
        self.assertIn("Simulador finalizado.", output.getvalue())


if __name__ == "__main__":
    unittest.main()

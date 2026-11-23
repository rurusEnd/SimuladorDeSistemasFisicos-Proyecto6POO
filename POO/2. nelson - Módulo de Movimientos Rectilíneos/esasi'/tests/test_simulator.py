import csv
import math
import tempfile
import unittest
from pathlib import Path

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

    def test_linear_motion_with_zero_acceleration_is_mru(self):
        system = LinearMotion(initial_position=2, initial_velocity=3, acceleration=0)

        self.assertEqual(system.calculate_position(2), 8)
        self.assertEqual(system.calculate_velocity(2), 3)
        self.assertEqual(system.calculate_acceleration(2), 0)

    def test_free_fall_stops_at_ground(self):
        system = FreeFall(initial_height=4)

        self.assertAlmostEqual(system.calculate_position(0.5), 2.77375)
        self.assertEqual(system.calculate_velocity(1), 0)
        self.assertEqual(system.calculate_acceleration(1), 0)

    def test_projectile_calculates_two_dimensional_motion_and_impact(self):
        system = ProjectileMotion(
            initial_height=10, initial_speed=10, angle_degrees=30
        )
        x, y = system.calculate_position(1)

        self.assertAlmostEqual(x, 10 * math.cos(math.radians(30)))
        self.assertAlmostEqual(y, 10 + 5 - 0.5 * 9.81)
        self.assertEqual(system.calculate_acceleration(100), (0, 0))

    def test_circular_motion_has_centripetal_acceleration(self):
        system = CircularMotion(radius=2, angular_velocity=3)

        self.assertEqual(system.calculate_position(0), (2, 0))
        self.assertEqual(system.calculate_velocity(0), (0, 6))
        self.assertEqual(system.calculate_acceleration(0), (-18, 0))

    def test_oscillator_calculates_simple_harmonic_motion(self):
        system = Oscillator(amplitude=2, angular_frequency=3)

        self.assertEqual(system.calculate_position(0), 2)
        self.assertEqual(system.calculate_velocity(0), 0)
        self.assertEqual(system.calculate_acceleration(0), -18)

    def test_system_rejects_invalid_time_and_parameters(self):
        system = LinearMotion(0, 1, 0)

        with self.assertRaises(ValueError):
            system.calculate_position(-1)
        with self.assertRaises(ValueError):
            FreeFall(initial_height=-1)


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


if __name__ == "__main__":
    unittest.main()

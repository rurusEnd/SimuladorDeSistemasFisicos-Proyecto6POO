import tkinter as tk
from math import isfinite
from tkinter import filedialog, messagebox, ttk

from models.circular_motion import CircularMotion
from models.free_fall import FreeFall
from models.linear_motion import LinearMotion
from models.oscillator import Oscillator
from models.physical_system import PhysicalSystem, PhysicalValue
from models.projectile import ProjectileMotion
from models.simulation import Simulation

MODEL_FIELDS = {
    "Movimiento rectilíneo (MRUV)": [
        ("initial_position", "Posición inicial x₀ (m)", "0"),
        ("initial_velocity", "Velocidad inicial v₀ (m/s)", "5"),
        ("acceleration", "Aceleración a (m/s²)", "2"),
    ],
    "Caída libre": [
        ("initial_height", "Altura inicial h₀ (m)", "10"),
        ("gravity", "Gravedad g (m/s²)", "9.81"),
    ],
    "Movimiento parabólico": [
        ("initial_x", "Posición inicial x₀ (m)", "0"),
        ("initial_height", "Altura inicial y₀ (m)", "0"),
        ("initial_speed", "Rapidez inicial v₀ (m/s)", "20"),
        ("angle_degrees", "Ángulo de lanzamiento (grados)", "45"),
        ("gravity", "Gravedad g (m/s²)", "9.81"),
    ],
    "Movimiento circular": [
        ("radius", "Radio r (m)", "2"),
        ("angular_velocity", "Velocidad angular ω (rad/s)", "2"),
        ("initial_angle_degrees", "Ángulo inicial (grados)", "0"),
        ("center_x", "Centro x (m)", "0"),
        ("center_y", "Centro y (m)", "0"),
        ("angular_acceleration", "Aceleración angular (rad/s²)", "0"),
    ],
    "Oscilador armónico": [
        ("amplitude", "Amplitud A (m)", "2"),
        ("angular_frequency", "Frecuencia angular ω (rad/s)", "2"),
        ("phase_degrees", "Fase inicial (grados)", "0"),
    ],
}

COLORS = ("#2563eb", "#dc2626", "#059669", "#9333ea", "#ea580c", "#0891b2")
MAX_ANIMATION_FRAMES = 120


def create_physical_system(
    model_name: str,
    parameters: dict[str, float],
    *,
    oscillator_uses_spring: bool = False,
    name: str = "",
) -> PhysicalSystem:
    if model_name == "Movimiento rectilíneo (MRUV)":
        system = LinearMotion(
            parameters["initial_position"],
            parameters["initial_velocity"],
            parameters["acceleration"],
        )
    elif model_name == "Caída libre":
        system = FreeFall(parameters["initial_height"], parameters["gravity"])
    elif model_name == "Movimiento parabólico":
        system = ProjectileMotion(
            initial_height=parameters["initial_height"],
            initial_speed=parameters["initial_speed"],
            angle_degrees=parameters["angle_degrees"],
            gravity=parameters["gravity"],
            initial_x=parameters["initial_x"],
        )
    elif model_name == "Movimiento circular":
        system = CircularMotion(
            radius=parameters["radius"],
            angular_velocity=parameters["angular_velocity"],
            initial_angle_degrees=parameters["initial_angle_degrees"],
            center_x=parameters["center_x"],
            center_y=parameters["center_y"],
            angular_acceleration=parameters["angular_acceleration"],
        )
    elif model_name == "Oscilador armónico":
        if oscillator_uses_spring:
            system = Oscillator(
                amplitude=parameters["amplitude"],
                phase_degrees=parameters["phase_degrees"],
                mass=parameters["mass"],
                spring_constant=parameters["spring_constant"],
            )
        else:
            system = Oscillator(
                amplitude=parameters["amplitude"],
                angular_frequency=parameters["angular_frequency"],
                phase_degrees=parameters["phase_degrees"],
            )
    else:
        raise ValueError(f"Modelo desconocido: {model_name}")

    if name.strip():
        system.name = name
    return system


def position_coordinates(
    system: PhysicalSystem, position: PhysicalValue
) -> tuple[float, float]:
    if isinstance(position, tuple):
        return position[0], position[1]
    if isinstance(system, FreeFall):
        return 0.0, position
    return position, 0.0


def format_value(value: PhysicalValue) -> str:
    if isinstance(value, tuple):
        return "(" + ", ".join(f"{component:.2f}" for component in value) + ")"
    return f"{value:.2f}"


class SimulatorWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simulador visual de sistemas físicos")
        self.root.geometry("1120x760")
        self.root.minsize(900, 620)

        self.systems: list[tuple[str, PhysicalSystem]] = []
        self.simulation: Simulation | None = None
        self.animation_after: str | None = None
        self.frame_indices: list[int] = []
        self.animation_frame = 0
        self.plot_points: dict[str, list[tuple[float, float]]] = {}
        self.plot_bounds = (-1.0, 1.0, -1.0, 1.0)
        self.system_list: tk.Listbox | None = None
        self.parameter_vars: dict[str, tk.StringVar] = {}
        self.oscillator_mode_var = tk.StringVar(value="Frecuencia angular")

        self._build_layout()
        self._add_default_systems()

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=14)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(2, weight=1)

        title = ttk.Label(
            container,
            text="Simulador de sistemas físicos",
            font=("Segoe UI", 20, "bold"),
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w")
        subtitle = ttk.Label(
            container,
            text="Empieza con una pelota; las opciones para comparar son opcionales.",
        )
        subtitle.grid(row=1, column=0, columnspan=2, sticky="w", pady=(2, 12))

        controls = ttk.Frame(container, width=390)
        controls.grid(row=2, column=0, sticky="nsew", padx=(0, 14))
        controls.grid_propagate(False)

        self.quick_help = ttk.LabelFrame(controls, text="Prueba rápida", padding=12)
        self.quick_help.pack(fill="x")
        self.quick_description = ttk.Label(
            self.quick_help,
            text="Hay una pelota lista para caer desde 10 metros.",
            wraplength=340,
        )
        self.quick_description.pack(anchor="w", pady=(0, 10))
        ttk.Button(
            self.quick_help,
            text="Más opciones: agregar y comparar",
            command=self._show_advanced_options,
        ).pack(fill="x")

        # Las opciones avanzadas quedan ocultas al inicio y usan esta misma ventana.
        self.advanced_frame = ttk.LabelFrame(
            controls, text="Agregar y comparar movimientos", padding=8
        )
        self._build_advanced_panel()
        self.advanced_frame.pack_forget()

        self.settings_frame = ttk.LabelFrame(controls, text="Tiempo", padding=12)
        self.settings_frame.pack(fill="x", pady=(10, 0))
        self.duration_var = tk.StringVar(value="1")
        self.time_step_var = tk.StringVar(value="0.05")
        self._add_setting(self.settings_frame, "Duración (s)", self.duration_var)
        self._add_setting(self.settings_frame, "Intervalo (s)", self.time_step_var)
        self.run_button = ttk.Button(
            self.settings_frame,
            text="▶  Ver caer la pelota",
            command=self._run_simulation,
        )
        self.run_button.pack(fill="x", pady=(10, 0))
        self.export_button = ttk.Button(
            self.settings_frame,
            text="Guardar resultados CSV",
            command=self._save_csv,
            state="disabled",
        )
        self.export_button.pack(fill="x", pady=(6, 0))

        display = ttk.Frame(container)
        display.grid(row=2, column=1, sticky="nsew")
        display.columnconfigure(0, weight=1)
        display.rowconfigure(0, weight=3)
        display.rowconfigure(2, weight=2)

        self.canvas = tk.Canvas(
            display,
            background="#f8fafc",
            highlightthickness=1,
            highlightbackground="#cbd5e1",
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.time_label = ttk.Label(
            display, text="Presiona «Ver caer la pelota» para empezar."
        )
        self.time_label.grid(row=1, column=0, sticky="w", pady=8)

        result_frame = ttk.LabelFrame(display, text="Resultados al finalizar", padding=6)
        result_frame.grid(row=2, column=0, sticky="nsew")
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        columns = ("system", "position", "velocity", "acceleration")
        self.results_table = ttk.Treeview(
            result_frame, columns=columns, show="headings", height=5
        )
        for column, heading, width in (
            ("system", "Experimento", 180),
            ("position", "Posición", 200),
            ("velocity", "Velocidad", 160),
            ("acceleration", "Aceleración", 140),
        ):
            self.results_table.heading(column, text=heading)
            self.results_table.column(column, width=width, anchor="center")
        self.results_table.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            result_frame, orient="vertical", command=self.results_table.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.results_table.configure(yscrollcommand=scrollbar.set)

        self.status_var = tk.StringVar(value="Listo.")
        ttk.Label(container, textvariable=self.status_var).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )

    def _build_advanced_panel(self) -> None:
        ttk.Label(
            self.advanced_frame,
            text="La pelota de prueba se conserva. Agrega otros movimientos "
            "si quieres compararlos.",
            wraplength=350,
        ).pack(anchor="w", pady=(0, 8))
        experiment = ttk.LabelFrame(
            self.advanced_frame, text="Nuevo movimiento", padding=8
        )
        experiment.pack(fill="x")
        ttk.Label(experiment, text="Tipo de movimiento").pack(anchor="w")
        self.model_var = tk.StringVar(value=next(iter(MODEL_FIELDS)))
        model_picker = ttk.Combobox(
            experiment,
            textvariable=self.model_var,
            values=list(MODEL_FIELDS),
            state="readonly",
        )
        model_picker.pack(fill="x", pady=(2, 8))
        model_picker.bind(
            "<<ComboboxSelected>>", lambda _event: self._render_parameter_fields()
        )

        self.parameter_frame = ttk.Frame(experiment)
        self.parameter_frame.pack(fill="x")
        ttk.Label(experiment, text="Nombre (opcional)").pack(anchor="w", pady=(8, 0))
        self.name_var = tk.StringVar()
        ttk.Entry(experiment, textvariable=self.name_var).pack(fill="x", pady=(2, 8))
        ttk.Button(
            experiment, text="Agregar movimiento", command=self._add_system
        ).pack(fill="x")

        registered = ttk.LabelFrame(
            self.advanced_frame, text="Movimientos agregados", padding=6
        )
        registered.pack(fill="both", expand=True, pady=(8, 0))
        self.system_list = tk.Listbox(registered, height=8, activestyle="dotbox")
        self.system_list.pack(fill="both", expand=True)
        ttk.Button(
            registered, text="Quitar seleccionado", command=self._remove_system
        ).pack(fill="x", pady=(6, 0))

        self._render_parameter_fields()
        for name, system in self.systems:
            self.system_list.insert("end", f"{name} — {self._model_label(system)}")
        ttk.Button(
            self.advanced_frame,
            text="Volver a la prueba rápida",
            command=self._show_quick_options,
        ).pack(fill="x", pady=(8, 0))

    def _show_advanced_options(self) -> None:
        self.quick_help.pack_forget()
        self.advanced_frame.pack(
            fill="both", expand=True, before=self.settings_frame
        )
        self.run_button.configure(text="▶  Simular y comparar")
        self.status_var.set("Puedes agregar modelos; el botón de abajo los simula juntos.")

    def _show_quick_options(self) -> None:
        self.advanced_frame.pack_forget()
        self.quick_help.pack(fill="x", before=self.settings_frame)
        self._update_quick_summary()
        self.status_var.set("La pelota de prueba está lista.")

    @staticmethod
    def _add_setting(parent: ttk.LabelFrame, label: str, variable: tk.StringVar) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label).pack(side="left")
        ttk.Entry(row, textvariable=variable, width=10).pack(side="right")

    def _render_parameter_fields(self) -> None:
        for child in self.parameter_frame.winfo_children():
            child.destroy()
        self.parameter_vars.clear()

        model_name = self.model_var.get()
        field_specs = list(MODEL_FIELDS[model_name])
        if model_name == "Oscilador armónico":
            ttk.Label(self.parameter_frame, text="Cómo definirlo").pack(anchor="w")
            mode_picker = ttk.Combobox(
                self.parameter_frame,
                textvariable=self.oscillator_mode_var,
                values=("Frecuencia angular", "Masa y resorte"),
                state="readonly",
            )
            mode_picker.pack(fill="x", pady=(2, 6))
            mode_picker.bind(
                "<<ComboboxSelected>>",
                lambda _event: self._render_parameter_fields(),
            )
            if self.oscillator_mode_var.get() == "Masa y resorte":
                field_specs = [
                    ("amplitude", "Amplitud A (m)", "2"),
                    ("mass", "Masa m (kg)", "1"),
                    ("spring_constant", "Constante k (N/m)", "4"),
                    ("phase_degrees", "Fase inicial (grados)", "0"),
                ]

        for key, label, default in field_specs:
            row = ttk.Frame(self.parameter_frame)
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=label).pack(side="left")
            variable = tk.StringVar(value=default)
            ttk.Entry(row, textvariable=variable, width=10).pack(side="right")
            self.parameter_vars[key] = variable

    def _add_default_systems(self) -> None:
        self._register_system(FreeFall(10), "Pelota (caída libre)")

    def _register_system(self, system: PhysicalSystem, requested_name: str) -> None:
        existing_names = {name for name, _ in self.systems}
        name = requested_name.strip() or system.name
        unique_name = name
        suffix = 2
        while unique_name in existing_names:
            unique_name = f"{name} ({suffix})"
            suffix += 1
        system.name = unique_name
        self.systems.append((unique_name, system))
        if self.system_list is not None and self.system_list.winfo_exists():
            self.system_list.insert("end", f"{unique_name} — {self._model_label(system)}")
        self._update_quick_summary()

    def _update_quick_summary(self) -> None:
        count = len(self.systems)
        if count == 0:
            self.quick_description.configure(text="Agrega un movimiento desde «Más opciones».")
            self.run_button.configure(state="disabled")
        elif count == 1:
            name, system = self.systems[0]
            if isinstance(system, FreeFall):
                description = (
                    f"Hay una pelota lista para caer desde "
                    f"{system.initial_height:g} metros."
                )
                button_text = "▶  Ver caer la pelota"
            else:
                description = f"Hay un experimento listo: {name}."
                button_text = "▶  Simular experimento"
            self.quick_description.configure(text=description)
            self.run_button.configure(text=button_text, state="normal")
        else:
            self.quick_description.configure(
                text=f"Hay {count} movimientos listos para simular y comparar."
            )
            self.run_button.configure(text="▶  Simular y comparar", state="normal")

    @staticmethod
    def _model_label(system: PhysicalSystem) -> str:
        for label, model_type in (
            ("Movimiento rectilíneo (MRUV)", LinearMotion),
            ("Caída libre", FreeFall),
            ("Movimiento parabólico", ProjectileMotion),
            ("Movimiento circular", CircularMotion),
            ("Oscilador armónico", Oscillator),
        ):
            if isinstance(system, model_type):
                return label
        return "Sistema físico"

    def _add_system(self) -> None:
        try:
            parameters = {
                key: float(variable.get())
                for key, variable in self.parameter_vars.items()
            }
            if not all(isfinite(value) for value in parameters.values()):
                raise ValueError("Los parámetros deben ser números finitos.")

            model_name = self.model_var.get()
            system = create_physical_system(
                model_name,
                parameters,
                oscillator_uses_spring=(
                    model_name == "Oscilador armónico"
                    and self.oscillator_mode_var.get() == "Masa y resorte"
                ),
                name=self.name_var.get(),
            )
        except (KeyError, TypeError, ValueError) as error:
            messagebox.showerror("Parámetros inválidos", str(error), parent=self.root)
            return

        requested_name = self.name_var.get().strip() or system.name
        self._register_system(system, requested_name)
        self.name_var.set("")
        self.status_var.set(f"Agregado: {system.name}.")

    def _remove_system(self) -> None:
        if self.system_list is None:
            return
        selection = self.system_list.curselection()
        if not selection:
            self.status_var.set("Selecciona un experimento para quitarlo.")
            return
        index = selection[0]
        self.system_list.delete(index)
        self.systems.pop(index)
        self._update_quick_summary()
        self.status_var.set("Experimento quitado.")

    def _run_simulation(self) -> None:
        self._cancel_animation()
        if not self.systems:
            messagebox.showerror(
                "Sin experimentos",
                "Agrega al menos un sistema antes de simular.",
                parent=self.root,
            )
            return
        try:
            duration = float(self.duration_var.get())
            time_step = float(self.time_step_var.get())
            simulation = Simulation("Simulación visual")
            for name, system in self.systems:
                simulation.add_system(system, name=name)
            # Simulation calcula la física; la interfaz solo presenta sus resultados.
            simulation.simulate(duration, time_step)
        except (ArithmeticError, TypeError, ValueError) as error:
            messagebox.showerror("No se pudo simular", str(error), parent=self.root)
            self.status_var.set("Revisa la duración, el intervalo y los experimentos.")
            return

        self.simulation = simulation
        self._prepare_animation()
        self._clear_results()
        self.export_button.configure(state="normal")
        self.animation_frame = 0
        self.status_var.set(
            f"{len(self.systems)} experimento(s), "
            f"{len(next(iter(simulation.history.values())))} muestras."
        )
        self._animate_next_frame()

    def _prepare_animation(self) -> None:
        assert self.simulation is not None
        total_samples = len(next(iter(self.simulation.history.values())))
        frame_count = min(total_samples, MAX_ANIMATION_FRAMES)
        if frame_count == 1:
            self.frame_indices = [0]
        else:
            # Se conservan todas las muestras; solo se limitan los cuadros animados.
            self.frame_indices = [
                round(index * (total_samples - 1) / (frame_count - 1))
                for index in range(frame_count)
            ]

        raw_points: dict[str, list[tuple[float, float]]] = {}
        largest_coordinate = 1.0
        for name, system in self.systems:
            positions = [
                position_coordinates(system, result.position)
                for result in self.simulation.history[name]
            ]
            raw_points[name] = positions
            for x, y in positions:
                largest_coordinate = max(largest_coordinate, abs(x), abs(y))

        # Esta escala es visual: no modifica los valores físicos guardados.
        self.plot_points = {
            name: [(x / largest_coordinate, y / largest_coordinate) for x, y in points]
            for name, points in raw_points.items()
        }
        all_points = [point for points in self.plot_points.values() for point in points]
        min_x = min(point[0] for point in all_points)
        max_x = max(point[0] for point in all_points)
        min_y = min(point[1] for point in all_points)
        max_y = max(point[1] for point in all_points)
        if max_x - min_x < 0.1:
            min_x -= 0.5
            max_x += 0.5
        if max_y - min_y < 0.1:
            min_y -= 0.5
            max_y += 0.5
        self.plot_bounds = (min_x, max_x, min_y, max_y)

    def _canvas_point(self, point: tuple[float, float]) -> tuple[float, float]:
        width = max(self.canvas.winfo_width(), 300)
        height = max(self.canvas.winfo_height(), 250)
        min_x, max_x, min_y, max_y = self.plot_bounds
        margin = 48
        scale = min(
            (width - 2 * margin) / (max_x - min_x),
            (height - 2 * margin) / (max_y - min_y),
        )
        plot_width = (max_x - min_x) * scale
        plot_height = (max_y - min_y) * scale
        offset_x = (width - plot_width) / 2
        offset_y = (height - plot_height) / 2
        x = offset_x + (point[0] - min_x) * scale
        y = height - offset_y - (point[1] - min_y) * scale
        return x, y

    def _animate_next_frame(self) -> None:
        if self.simulation is None or self.animation_frame >= len(self.frame_indices):
            self._show_final_results()
            return

        sample_index = self.frame_indices[self.animation_frame]
        self.canvas.delete("all")
        self._draw_axes()
        for system_index, (name, _system) in enumerate(self.systems):
            color = COLORS[system_index % len(COLORS)]
            points = self.plot_points[name][: sample_index + 1]
            canvas_points = [self._canvas_point(point) for point in points]
            if len(canvas_points) > 1:
                flattened = [coordinate for point in canvas_points for coordinate in point]
                self.canvas.create_line(
                    *flattened, fill=color, width=2, smooth=True
                )
            x, y = canvas_points[-1]
            self.canvas.create_oval(
                x - 9,
                y - 9,
                x + 9,
                y + 9,
                fill=color,
                outline="white",
                width=2,
            )
            self.canvas.create_text(
                14,
                14 + system_index * 22,
                anchor="w",
                text=name,
                fill=color,
                font=("Segoe UI", 9, "bold"),
            )

        result = next(iter(self.simulation.history.values()))[sample_index]
        self.time_label.configure(text=f"Tiempo simulado: {result.time:.2f} s")
        self.animation_frame += 1
        if self.animation_frame < len(self.frame_indices):
            self.animation_after = self.root.after(35, self._animate_next_frame)
        else:
            self.animation_after = None
            self._show_final_results()

    def _draw_axes(self) -> None:
        width = max(self.canvas.winfo_width(), 300)
        height = max(self.canvas.winfo_height(), 250)
        min_x, max_x, min_y, max_y = self.plot_bounds
        origin = self._canvas_point((0, 0))
        if min_y <= 0 <= max_y:
            self.canvas.create_line(
                32, origin[1], width - 18, origin[1], fill="#94a3b8", dash=(4, 4)
            )
        if min_x <= 0 <= max_x:
            self.canvas.create_line(
                origin[0], 24, origin[0], height - 24, fill="#94a3b8", dash=(4, 4)
            )
        self.canvas.create_text(
            width - 16, height - 12, text="x", fill="#64748b", anchor="e"
        )
        self.canvas.create_text(12, 14, text="y", fill="#64748b", anchor="w")

    def _clear_results(self) -> None:
        for item in self.results_table.get_children():
            self.results_table.delete(item)

    def _show_final_results(self) -> None:
        if self.simulation is None:
            return
        self._clear_results()
        for name, result in self.simulation.latest_results().items():
            self.results_table.insert(
                "",
                "end",
                values=(
                    name,
                    format_value(result.position),
                    format_value(result.velocity),
                    format_value(result.acceleration),
                ),
            )
        self.status_var.set("Animación terminada. Los resultados finales aparecen abajo.")

    def _save_csv(self) -> None:
        if self.simulation is None:
            return
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Guardar resultados de la simulación",
            defaultextension=".csv",
            initialfile="resultados.csv",
            filetypes=(("Archivo CSV", "*.csv"),),
        )
        if not path:
            return
        try:
            saved_path = self.simulation.save_csv(path)
        except (OSError, ValueError) as error:
            messagebox.showerror("No se pudo guardar", str(error), parent=self.root)
            return
        self.status_var.set(f"Resultados guardados en {saved_path}.")

    def _cancel_animation(self) -> None:
        if self.animation_after is not None:
            self.root.after_cancel(self.animation_after)
            self.animation_after = None


def main() -> None:
    root = tk.Tk()
    SimulatorWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import math
from .sistema_fisico import SistemaFisico


class MovimientoParabolico(SistemaFisico):
    """
    Movimiento de proyectil en dos dimensiones.

    Ecuaciones:
        x(t) = x0 + v0*cos(theta)*t
        y(t) = y0 + v0*sin(theta)*t - 0.5*g*t^2
    """

    def __init__(self, nombre: str, x0: float = 0.0, y0: float = 0.0,
                 v0: float = 0.0, angulo_grados: float = 0.0,
                 gravedad: float = 9.8):
        super().__init__(nombre)

        if v0 < 0:
            raise ValueError("La velocidad inicial no puede ser negativa.")
        if gravedad <= 0:
            raise ValueError("La gravedad debe ser mayor que cero.")

        self.x0 = x0
        self.y0 = y0
        self.v0 = v0
        self.angulo_grados = angulo_grados
        self.gravedad = gravedad

        self.angulo_rad = math.radians(angulo_grados)
        self.vx0 = v0 * math.cos(self.angulo_rad)
        self.vy0 = v0 * math.sin(self.angulo_rad)

    @staticmethod
    def _validar_tiempo(t: float) -> None:
        if t < 0:
            raise ValueError("El tiempo no puede ser negativo.")

    def calcular_posicion(self, t: float) -> tuple[float, float]:
        self._validar_tiempo(t)
        x = self.x0 + self.vx0 * t
        y = self.y0 + self.vy0 * t - 0.5 * self.gravedad * t * t
        return x, y

    def calcular_velocidad(self, t: float) -> tuple[float, float]:
        self._validar_tiempo(t)
        vx = self.vx0
        vy = self.vy0 - self.gravedad * t
        return vx, vy

    def calcular_aceleracion(self, t: float) -> tuple[float, float]:
        self._validar_tiempo(t)
        return 0.0, -self.gravedad

    def simular(self, t_max: float, pasos: int = 100) -> list[dict]:
        if t_max < 0:
            raise ValueError("El tiempo máximo no puede ser negativo.")
        if pasos <= 0:
            raise ValueError("El número de pasos debe ser mayor que cero.")

        dt = t_max / pasos
        resultados = []

        for i in range(pasos + 1):
            t = i * dt
            resultados.append({
                "tiempo": t,
                "posicion": self.calcular_posicion(t),
                "velocidad": self.calcular_velocidad(t),
                "aceleracion": self.calcular_aceleracion(t),
            })

        return resultados
import math
from .sistema_fisico import SistemaFisico


class MovimientoCircular(SistemaFisico):
    """
    Movimiento circular con velocidad angular constante o con aceleración angular.

    Ecuaciones:
        theta(t) = phi0 + omega*t + 0.5*alpha*t^2
        x(t) = cx + R*cos(theta(t))
        y(t) = cy + R*sin(theta(t))
    """

    def __init__(self, nombre: str, radio: float, velocidad_angular: float,
                 angulo_inicial: float = 0.0, centro_x: float = 0.0,
                 centro_y: float = 0.0, aceleracion_angular: float = 0.0):
        super().__init__(nombre)

        if radio <= 0:
            raise ValueError("El radio debe ser mayor que cero.")

        self.radio = radio
        self.velocidad_angular = velocidad_angular
        self.angulo_inicial = angulo_inicial
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.aceleracion_angular = aceleracion_angular

    @staticmethod
    def _validar_tiempo(t: float) -> None:
        if t < 0:
            raise ValueError("El tiempo no puede ser negativo.")

    def _theta(self, t: float) -> float:
        return (self.angulo_inicial
                + self.velocidad_angular * t
                + 0.5 * self.aceleracion_angular * t * t)

    def _omega_t(self, t: float) -> float:
        return self.velocidad_angular + self.aceleracion_angular * t

    def calcular_posicion(self, t: float) -> tuple[float, float]:
        self._validar_tiempo(t)
        theta = self._theta(t)
        x = self.centro_x + self.radio * math.cos(theta)
        y = self.centro_y + self.radio * math.sin(theta)
        return x, y

    def calcular_velocidad(self, t: float) -> tuple[float, float]:
        self._validar_tiempo(t)
        theta = self._theta(t)
        omega_t = self._omega_t(t)
        vx = -self.radio * omega_t * math.sin(theta)
        vy = self.radio * omega_t * math.cos(theta)
        return vx, vy

    def calcular_aceleracion(self, t: float) -> tuple[float, float]:
        self._validar_tiempo(t)
        theta = self._theta(t)
        omega_t = self._omega_t(t)

        # Aceleración tangencial + centrípeta
        ax = -self.radio * (self.aceleracion_angular * math.sin(theta)
                            + omega_t * omega_t * math.cos(theta))
        ay = self.radio * (self.aceleracion_angular * math.cos(theta)
                           - omega_t * omega_t * math.sin(theta))
        return ax, ay

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
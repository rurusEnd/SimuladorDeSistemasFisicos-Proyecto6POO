import math
from .sistema_fisico import SistemaFisico


class Oscilador(SistemaFisico):
    """
    Oscilador armónico simple masa-resorte.

    Ecuaciones:
        omega = sqrt(k / m)
        x(t) = A*cos(omega*t + fase)
        v(t) = -A*omega*sin(omega*t + fase)
        a(t) = -omega^2 * x(t)
    """

    def __init__(self, nombre: str, masa: float, constante_resorte: float,
                 amplitud: float, fase: float = 0.0):
        super().__init__(nombre)

        if masa <= 0:
            raise ValueError("La masa debe ser mayor que cero.")
        if constante_resorte <= 0:
            raise ValueError("La constante del resorte debe ser mayor que cero.")
        if amplitud < 0:
            raise ValueError("La amplitud no puede ser negativa.")

        self.masa = masa
        self.constante_resorte = constante_resorte
        self.amplitud = amplitud
        self.fase = fase

        self.omega = math.sqrt(constante_resorte / masa)

    @staticmethod
    def _validar_tiempo(t: float) -> None:
        if t < 0:
            raise ValueError("El tiempo no puede ser negativo.")

    def calcular_posicion(self, t: float) -> float:
        self._validar_tiempo(t)
        return self.amplitud * math.cos(self.omega * t + self.fase)

    def calcular_velocidad(self, t: float) -> float:
        self._validar_tiempo(t)
        return -self.amplitud * self.omega * math.sin(self.omega * t + self.fase)

    def calcular_aceleracion(self, t: float) -> float:
        self._validar_tiempo(t)
        return -(self.omega ** 2) * self.calcular_posicion(t)

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
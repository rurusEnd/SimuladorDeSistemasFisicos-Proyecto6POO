# Simulador de sistemas físicos

Simulador interactivo en Python para el Proyecto 6 de POO. Implementa una
jerarquía polimórfica de sistemas físicos, calcula posición, velocidad y
aceleración, guarda muestras en CSV y permite comparar los sistemas.

## Requisitos

- Python 3.10 o posterior
- No requiere dependencias externas

## Ejecutar

Desde la carpeta del proyecto:

```powershell
python main.py
```

El programa inicia con ejemplos de caída libre y movimiento rectilíneo. En el
menú puedes agregar cualquiera de estos modelos:

1. Movimiento rectilíneo uniformemente variado (MRUV)
2. Caída libre
3. Movimiento parabólico
4. Movimiento circular
5. Oscilador armónico

Al ejecutar una simulación se indica la duración y el intervalo entre muestras.
El estado final se compara automáticamente; también puedes volver a consultar
la comparación o guardar todo el historial en `resultados.csv`.

Los tiempos deben ser finitos y no negativos, el intervalo debe ser mayor que
cero y cada simulación está limitada a 100 000 muestras.

## Probar

```powershell
python -m unittest discover -s tests -v
```

# esta es una prueba en al reunion

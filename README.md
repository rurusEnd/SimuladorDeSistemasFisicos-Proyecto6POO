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

También puedes iniciar la interfaz gráfica:

```powershell
python gui.py
```

La ventana abre una prueba rápida de caída libre: presiona **Ver caer la pelota**
para iniciar la animación. Todo ocurre en la misma ventana. Si quieres, en
**Más opciones** puedes agregar otros movimientos y compararlos; luego puedes
volver a la prueba rápida. Al final se muestran posición, velocidad y
aceleración, y puedes guardar los resultados en CSV. La interfaz usa Tkinter,
incluido en las instalaciones habituales de Python para Windows.

### Cómo leer el código de la interfaz

- `create_physical_system()` convierte los datos del formulario en una instancia
  del modelo elegido.
- `_run_simulation()` entrega los sistemas a `Simulation`; las fórmulas físicas
  siguen en `models/`, separadas de la interfaz.
- `_prepare_animation()` organiza las posiciones y limita los cuadros dibujados
  para que la animación no se vuelva lenta. No cambia los resultados físicos.
- `_animate_next_frame()` dibuja cada cuadro y, al terminar, llena la tabla con
  los resultados finales.

El programa inicia con ejemplos de caída libre y movimiento rectilíneo. En el
menú puedes agregar cualquiera de estos modelos:

1. Movimiento rectilíneo uniformemente variado (MRUV)
2. Caída libre
3. Movimiento parabólico
4. Movimiento circular
5. Oscilador armónico

El movimiento parabólico acepta posiciones iniciales horizontal y vertical.
El movimiento circular también permite definir el centro y la aceleración
angular. Para el oscilador puedes ingresar directamente la frecuencia angular
o calcularla a partir de la masa y la constante del resorte (`ω = √(k/m)`).

Al ejecutar una simulación se indica la duración y el intervalo entre muestras.
El estado final se compara automáticamente; también puedes volver a consultar
la comparación, ver el historial completo (opción 5) o guardar todo el
historial en `resultados.csv`.

Los tiempos deben ser finitos y no negativos, el intervalo debe ser mayor que
cero y cada simulación está limitada a 100 000 muestras.
Los parámetros también se validan al crear o actualizar un sistema: un dato
que no sea numérico produce `TypeError`; un valor no finito o fuera de rango
produce `ValueError`.

## Probar

```powershell
python -m unittest discover -s tests -v
```

## Integrantes y aportes verificados

Se revisaron los archivos entregados bajo `POO/` y se adaptaron al contrato
actual (`PhysicalSystem` y métodos en inglés) en lugar de copiar proyectos
completos encima del simulador.

| Integrante (según la carpeta) | Aporte asignado | Verificación e integración |
| --- | --- | --- |
| Nelson — módulo de movimientos rectilíneos | MRU y MRUV | Su `LinearMotion` usa las ecuaciones correctas; con aceleración cero representa MRU. Se integraron propiedades modificables y validadas en `models/linear_motion.py`. |
| Maycol — movimientos curvos y oscilatorios | Movimiento parabólico, circular y oscilador | Las entregas contienen las ecuaciones de esos tres modelos. Se integraron en `models/projectile.py`, `models/circular_motion.py` y `models/oscillator.py`; el oscilador acepta masa y constante del resorte (`ω = √(k/m)`). |
| Chalco — encapsulamiento, validaciones y errores | Validar tipos y rangos; proteger parámetros con propiedades | Su copia incluye validación explícita de tipos y propiedades con setters. Se integró ese enfoque en los modelos y en la clase `Simulation`; las entradas no numéricas generan `TypeError` y las fuera de rango `ValueError`. |
| Angel — interfaz de consola y menú | Captura de parámetros, ejecución y consulta de resultados | Sus menús muestran el flujo previsto, pero el menú nuevo importa módulos `modelos` y `servicios` que no existen en el proyecto y no se conecta tal cual. `main.py` conserva el menú funcional e incluye alta de modelos, simulación, comparación, historial y exportación CSV. |

Las carpetas de Nelson y Chalco contienen copias completas del simulador, no
solo los módulos de su responsabilidad. Para evitar versiones duplicadas, la
versión ejecutable y sus pruebas están en la raíz y en `models/` y `tests/`.
En `POO/` solo aparecen entregas identificadas como integrantes 2, 3, 5 y 6;
no atribuí aportes a los integrantes 1 y 4 porque no hay carpetas suyas allí.

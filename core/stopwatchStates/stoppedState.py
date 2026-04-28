# Estado inicial del cronometro: nunca arranco o se acaba de reiniciar.

import time

from .stopwatchState import StopwatchState


class StoppedState(StopwatchState):

    def handleToggle(self, stopwatch) -> None:
        # Arrancamos de cero: marcamos el instante y pasamos a Corriendo.
        stopwatch._startTimestamp = time.perf_counter()
        stopwatch.setRunningState()

    def isRunning(self) -> bool:
        return False

    def recordLap(self, stopwatch) -> int:
        # Sin cronometro corriendo no hay vuelta que registrar.
        return -1

    def getCurrentElapsed(self, stopwatch) -> float:
        return stopwatch._accumulatedSeconds

    def __str__(self) -> str:
        return "Detenido"

# Estado del cronometro pausado: el tiempo no avanza pero el acumulado se conserva.

import time

from .stopwatchState import StopwatchState


class PausedState(StopwatchState):

    def handleToggle(self, stopwatch) -> None:
        # Al reanudar, marcamos un nuevo punto de inicio y volvemos a Corriendo.
        stopwatch._startTimestamp = time.perf_counter()
        stopwatch.setRunningState()

    def isRunning(self) -> bool:
        return False

    def recordLap(self, stopwatch) -> int:
        return -1

    def getCurrentElapsed(self, stopwatch) -> float:
        return stopwatch._accumulatedSeconds

    def __str__(self) -> str:
        return "Pausado"

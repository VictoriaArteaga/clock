# Estado del cronometro corriendo: el tiempo avanza y se pueden registrar vueltas.

import time

from .stopwatchState import StopwatchState


class RunningState(StopwatchState):

    def handleToggle(self, stopwatch) -> None:
        # Al pausar, sumamos el tramo actual al acumulado y cambiamos de estado.
        stopwatch._accumulatedSeconds += time.perf_counter() - stopwatch._startTimestamp
        stopwatch.setPausedState()

    def isRunning(self) -> bool:
        return True

    def recordLap(self, stopwatch) -> int:
        elapsedMs = stopwatch.getElapsedMs()
        # Agregamos al final de la lista circular doble que guarda las vueltas.
        stopwatch._lapTimes.insertTimeAtEnd(elapsedMs)
        return elapsedMs

    def getCurrentElapsed(self, stopwatch) -> float:
        # El tramo en curso aun no se acumulo, lo sumamos al vuelo.
        return stopwatch._accumulatedSeconds + (time.perf_counter() - stopwatch._startTimestamp)

    def __str__(self) -> str:
        return "Corriendo"

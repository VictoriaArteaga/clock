# Cronometro: mide intervalos con precision de centesimas y registra vueltas.

import time
from typing import List


class Stopwatch:
    """Cronometro con tres estados (detenido, corriendo, pausado) y vueltas."""

    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"

    def __init__(self):
        self._state: str = self.STOPPED
        # Marca de tiempo (perf_counter) cuando arranco o reanudo.
        self._startTimestamp: float = 0.0
        # Tiempo acumulado de tramos previos (sumado a la pausa).
        self._accumulatedSeconds: float = 0.0
        # Tiempos totales en milisegundos guardados al pulsar "Vuelta".
        self._lapTimes: List[int] = []

    @property
    def state(self) -> str:
        return self._state

    @property
    def laps(self) -> List[int]:
        return list(self._lapTimes)

    def isRunning(self) -> bool:
        return self._state == self.RUNNING

    def toggleRunning(self) -> None:
        """Alterna entre arrancar/reanudar y pausar."""
        if self._state == self.RUNNING:
            self._accumulatedSeconds += time.perf_counter() - self._startTimestamp
            self._state = self.PAUSED
        else:
            self._startTimestamp = time.perf_counter()
            self._state = self.RUNNING

    def reset(self) -> None:
        self._state = self.STOPPED
        self._startTimestamp = 0.0
        self._accumulatedSeconds = 0.0
        self._lapTimes.clear()

    def lap(self) -> int:
        """Registra el tiempo total como una vuelta y lo devuelve. -1 si no esta corriendo."""
        if self._state != self.RUNNING:
            return -1
        elapsed = self.getElapsedMs()
        self._lapTimes.append(elapsed)
        return elapsed

    def getElapsedMs(self) -> int:
        """Tiempo total transcurrido en milisegundos."""
        totalSeconds = self._accumulatedSeconds
        if self._state == self.RUNNING:
            totalSeconds += time.perf_counter() - self._startTimestamp
        return int(totalSeconds * 1000)

    @staticmethod
    def formatMs(milliseconds: int) -> str:
        """Convierte milisegundos a HH:MM:SS.CC (centesimas)."""
        centiseconds = (milliseconds // 10) % 100
        seconds = (milliseconds // 1000) % 60
        minutes = (milliseconds // 60_000) % 60
        hours = milliseconds // 3_600_000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

# Contexto del patron State para el cronometro: mide intervalos con precision
# de centesimas y delega cada operacion al estado actual (Detenido/Corriendo/Pausado).
# Las vueltas se guardan en una CycleTime (lista circular doblemente enlazada).

from typing import List

from clock.models.cycleTime import CycleTime
from .stopwatchStates.stoppedState import StoppedState
from .stopwatchStates.runningState import RunningState
from .stopwatchStates.pausedState import PausedState


class Stopwatch:
    """Cronometro como Contexto del patron State + registro de vueltas en CycleTime."""

    def __init__(self):
        # Instancias unicas de cada estado (se reutilizan al transicionar).
        self._stoppedState = StoppedState()
        self._runningState = RunningState()
        self._pausedState = PausedState()

        # Estado inicial: detenido.
        self._currentState = self._stoppedState

        # Datos compartidos que los estados leen y escriben.
        self._startTimestamp: float = 0.0       # marca de perf_counter al arrancar/reanudar.
        self._accumulatedSeconds: float = 0.0   # suma de tramos previos (tras pausas).
        # Tiempos totales (en ms) de cada vuelta, en una lista circular doble.
        self._lapTimes = CycleTime()

    # --- Transiciones de estado ----------------------------------------------
    def setStoppedState(self) -> None:
        self._currentState = self._stoppedState

    def setRunningState(self) -> None:
        self._currentState = self._runningState

    def setPausedState(self) -> None:
        self._currentState = self._pausedState

    @property
    def currentStateName(self) -> str:
        return str(self._currentState)

    @property
    def laps(self) -> List[int]:
        # Snapshot en orden de registro para que la UI lo muestre comodamente.
        return [node.getTime() for node in self._lapTimes]

    # --- Operaciones que delegan al estado actual ----------------------------
    def isRunning(self) -> bool:
        return self._currentState.isRunning()

    def toggleRunning(self) -> None:
        # Sin if/else: cada estado decide a cual transicionar.
        self._currentState.handleToggle(self)

    def lap(self) -> int:
        return self._currentState.recordLap(self)

    def getElapsedMs(self) -> int:
        return int(self._currentState.getCurrentElapsed(self) * 1000)

    # --- Reset (no depende del estado, siempre vuelve al inicial) ------------
    def reset(self) -> None:
        self._startTimestamp = 0.0
        self._accumulatedSeconds = 0.0
        self._lapTimes.clear()
        self.setStoppedState()

    @staticmethod
    def formatMs(milliseconds: int) -> str:
        """Convierte milisegundos a HH:MM:SS.CC (centesimas)."""
        centiseconds = (milliseconds // 10) % 100
        seconds = (milliseconds // 1000) % 60
        minutes = (milliseconds // 60_000) % 60
        hours = milliseconds // 3_600_000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

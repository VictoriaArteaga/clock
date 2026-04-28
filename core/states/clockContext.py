# Contexto del patron State: la GUI interactua con el reloj a traves de esta clase,
# que delega el comportamiento del tick al estado actual (RunningState / PausedState).

from datetime import datetime

from ..clock import Clock
from .pausedState import PausedState
from .runningState import RunningState


class ClockContext:

    def __init__(self):
        self.clock = Clock()

        self._pausedState = PausedState()
        self._runningState = RunningState()

        # Arrancamos en marcha y sincronizados con el sistema operativo.
        self._currentState = self._runningState
        self.syncToSystem()

    def setRunningState(self) -> None:
        self._currentState = self._runningState

    def setPausedState(self) -> None:
        self._currentState = self._pausedState

    def togglePause(self) -> None:
        # Sin if/else: cada estado sabe a cual transicionar al togglearse.
        self._currentState.handleToggle(self)

    def update(self) -> None:
        # El patron State decide si avanzar o no el motor.
        self._currentState.handleTick(self)

    def getTimeString(self) -> str:
        return self.clock.getTimeString()

    def getHms(self) -> tuple:
        return self.clock.getHms()

    def setTime(self, hour: int, minute: int, second: int) -> None:
        self.clock.setTime(hour, minute, second)

    def syncToSystem(self) -> None:
        # Reposiciona los punteros del motor en la hora actual del sistema.
        now = datetime.now()
        self.clock.setTime(now.hour, now.minute, now.second)

    def isRunning(self) -> bool:
        return self._currentState.isRunning()

    @property
    def currentStateName(self) -> str:
        return str(self._currentState)

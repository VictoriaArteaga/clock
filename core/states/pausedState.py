# Estado del reloj pausado: el tick no avanza nada; al togglear vuelve a Corriendo.

from .clockState import ClockState


class PausedState(ClockState):

    def handleTick(self, clockContext) -> None:
        pass

    def handleToggle(self, clockContext) -> None:
        clockContext.setRunningState()

    def isRunning(self) -> bool:
        return False

    def __str__(self) -> str:
        return "Pausado"

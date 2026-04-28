# Estado del reloj pausado: el tick no avanza el motor; el tiempo queda congelado.

from .clockState import ClockState


class PausedState(ClockState):

    def handleTick(self, clockContext) -> None:
        pass

    def isRunning(self) -> bool:
        return False

    def __str__(self) -> str:
        return "Pausado"

# Estado del reloj corriendo: cada tick avanza el motor en una unidad.

from .clockState import ClockState


class RunningState(ClockState):

    def handleTick(self, clockContext) -> None:
        clockContext.clock.tick()

    def isRunning(self) -> bool:
        return True

    def __str__(self) -> str:
        return "Corriendo"

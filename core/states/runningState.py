# Estado del reloj corriendo: cada tick avanza el motor; al togglear pasa a Pausado.

from .clockState import ClockState


class RunningState(ClockState):

    def handleTick(self, clockContext) -> None:
        clockContext.clock.tick()

    def handleToggle(self, clockContext) -> None:
        clockContext.setPausedState()

    def isRunning(self) -> bool:
        return True

    def __str__(self) -> str:
        return "Corriendo"

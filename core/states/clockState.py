# Interfaz abstracta del patron State: define como se comporta cada estado del reloj.
# Cada operacion del contexto que dependa del estado se delega aqui.

from abc import ABC, abstractmethod


class ClockState(ABC):

    @abstractmethod
    def handleTick(self, clockContext) -> None:
        """Comportamiento del reloj cuando llega un pulso de avance."""

    @abstractmethod
    def handleToggle(self, clockContext) -> None:
        """Comportamiento al pulsar Pausar/Reanudar (transicion al otro estado)."""

    @abstractmethod
    def isRunning(self) -> bool:
        """True si el estado representa el reloj en marcha."""

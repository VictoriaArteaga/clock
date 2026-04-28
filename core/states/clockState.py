# Interfaz abstracta del patron State: define como se comporta cada estado del reloj.

from abc import ABC, abstractmethod


class ClockState(ABC):

    @abstractmethod
    def handleTick(self, clockContext) -> None:
        """Comportamiento del reloj cuando llega un pulso de avance."""

    @abstractmethod
    def isRunning(self) -> bool:
        """True si el estado representa el reloj en marcha."""

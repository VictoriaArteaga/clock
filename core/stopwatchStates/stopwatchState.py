# Interfaz abstracta del patron State para el cronometro.
# Cada operacion del Stopwatch que dependa del estado se delega aqui, evitando
# las cadenas de if/else sobre constantes de tipo "stopped"/"running"/"paused".

from abc import ABC, abstractmethod


class StopwatchState(ABC):

    @abstractmethod
    def handleToggle(self, stopwatch) -> None:
        """Comportamiento al pulsar el boton Iniciar/Pausar."""

    @abstractmethod
    def isRunning(self) -> bool:
        """True si el cronometro esta avanzando ahora mismo."""

    @abstractmethod
    def recordLap(self, stopwatch) -> int:
        """Registra una vuelta y devuelve los ms transcurridos. -1 si no aplica."""

    @abstractmethod
    def getCurrentElapsed(self, stopwatch) -> float:
        """Segundos totales transcurridos en el momento de la consulta."""

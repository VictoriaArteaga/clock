# Esta clase representa los nodos, 
# en este caso unidades de tiempo: segundos, minutos y horas.

class UnitTime:

    def __init__(self, time):
        self._time: int = time
        self._prevTime: 'UnitTime' = None
        self._nextTime: 'UnitTime' = None

    # getters y setters de la clase.

    def getTime(self) -> int:
        return self._time
    
    def setTime(self, time) -> None:
        self._time = time

    def getPrevTime(self) -> 'UnitTime':
        return self._prevTime

    def setPrevTime(self, prevTime) -> None:
        self._prevTime = prevTime

    def getNextTime(self) -> 'UnitTime':
        return self._nextTime

    def setNextTime(self, nextTime) -> None:
        self._nextTime = nextTime
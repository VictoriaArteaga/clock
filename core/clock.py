# Motor del reloj: coordina los ciclos de segundos, minutos y horas.
# Cada ciclo es una CycleTime (lista circular doblemente enlazada) cuyo nodo
# "currentX" indica la posicion actual.

from ..models.cycleTime import CycleTime


class Clock:

    SECONDS_PER_CYCLE = 60
    MINUTES_PER_CYCLE = 60
    HOURS_PER_CYCLE = 24  # formato 24h para distinguir AM/PM.

    def __init__(self):
        # insertTimeAtBeginning siempre encabeza con el ultimo insertado, asi que
        # insertamos de mayor a menor para que .getNextTime() avance 0,1,2,...,N,0,...
        self.secondCycle = CycleTime()
        for secondValue in range(self.SECONDS_PER_CYCLE - 1, -1, -1):
            self.secondCycle.insertTimeAtBeginning(secondValue)

        self.minuteCycle = CycleTime()
        for minuteValue in range(self.MINUTES_PER_CYCLE - 1, -1, -1):
            self.minuteCycle.insertTimeAtBeginning(minuteValue)

        self.hourCycle = CycleTime()
        for hourValue in range(self.HOURS_PER_CYCLE - 1, -1, -1):
            self.hourCycle.insertTimeAtBeginning(hourValue)

        # Punteros que marcan el tiempo actual en cada ciclo.
        self.currentSecond = self.secondCycle.firstTime
        self.currentMinute = self.minuteCycle.firstTime
        self.currentHour = self.hourCycle.firstTime

    def tick(self) -> None:
        """Avanza un segundo. Cuando un ciclo se completa, dispara el siguiente."""
        self.currentSecond = self.currentSecond.getNextTime()
        if self.currentSecond == self.secondCycle.firstTime:
            self.currentMinute = self.currentMinute.getNextTime()
            if self.currentMinute == self.minuteCycle.firstTime:
                self.currentHour = self.currentHour.getNextTime()

    def getTimeString(self) -> str:
        """Devuelve la hora en formato HH:MM:SS."""
        return (f"{self.currentHour.getTime():02d}:"
                f"{self.currentMinute.getTime():02d}:"
                f"{self.currentSecond.getTime():02d}")

    def getHms(self) -> tuple:
        """Devuelve la hora actual como tupla (hora, minuto, segundo)."""
        return (self.currentHour.getTime(),
                self.currentMinute.getTime(),
                self.currentSecond.getTime())

    def setTime(self, hour: int, minute: int, second: int) -> None:
        """Reposiciona los punteros para que reflejen la hora indicada."""
        self.currentHour = self._findCycleNode(self.hourCycle, hour)
        self.currentMinute = self._findCycleNode(self.minuteCycle, minute)
        self.currentSecond = self._findCycleNode(self.secondCycle, second)

    @staticmethod
    def _findCycleNode(cycleList, targetValue):
        """Recorre la lista circular hasta hallar el nodo con `targetValue`."""
        currentNode = cycleList.firstTime
        startNode = currentNode
        while currentNode.getTime() != targetValue:
            currentNode = currentNode.getNextTime()
            if currentNode == startNode:
                # Una vuelta completa sin coincidir: devolvemos el head como fallback.
                return cycleList.firstTime
        return currentNode

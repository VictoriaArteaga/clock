# Modelo de alarmas: cada alarma es un dato simple y el AlarmManager las
# almacena en una CycleTime (lista circular doblemente enlazada).

import itertools
from dataclasses import dataclass
from typing import List, Optional

from .cycleTime import CycleTime


@dataclass
class Alarm:
    alarmId: int        # identificador unico para enlazar UI y modelo.
    name: str           # nombre que el usuario le pone (ej: "Despertador").
    hour: int
    minute: int
    second: int = 0
    isActive: bool = True

    def getTimeString(self) -> str:
        # El formulario solo pide horas y minutos, asi que mostramos HH:MM.
        return f"{self.hour:02d}:{self.minute:02d}"


class AlarmManager:
    """Mantiene las alarmas guardadas en una CycleTime y decide cuando suenan."""

    def __init__(self):
        # Lista circular doblemente enlazada de alarmas (cada nodo guarda un Alarm).
        self._alarmList = CycleTime()
        self._idCounter = itertools.count(1)
        # Memoria del ultimo (hora, minuto) que disparo, para no repetir
        # el sonido 60 veces dentro del mismo minuto.
        self._lastFiredMinute: Optional[tuple] = None

    @property
    def alarms(self) -> List[Alarm]:
        # Snapshot en orden de insercion para que la UI lo recorra comodamente.
        return [node.getTime() for node in self._alarmList]

    def add(self, name: str, hour: int, minute: int, second: int = 0) -> Alarm:
        newAlarm = Alarm(
            alarmId=next(self._idCounter),
            name=name or "Alarma",
            hour=hour, minute=minute, second=second,
        )
        # Las alarmas se agregan al final para conservar el orden de creacion.
        self._alarmList.insertTimeAtEnd(newAlarm)
        return newAlarm

    def remove(self, alarmId: int) -> None:
        for node in self._alarmList:
            if node.getTime().alarmId == alarmId:
                self._alarmList.removeTime(node)
                return

    def toggle(self, alarmId: int) -> None:
        for node in self._alarmList:
            alarm = node.getTime()
            if alarm.alarmId == alarmId:
                alarm.isActive = not alarm.isActive
                return

    def snooze(self, alarmId: int, currentTime: tuple, minutesAhead: int = 5) -> None:
        """Reprograma la alarma a (hora actual + minutos), reactivada y con segundo 0."""
        currentHour, currentMinute, _unusedSecond = currentTime
        totalMinutes = (currentHour * 60 + currentMinute + minutesAhead) % (24 * 60)
        newHour, newMinute = divmod(totalMinutes, 60)
        for node in self._alarmList:
            alarm = node.getTime()
            if alarm.alarmId == alarmId:
                alarm.hour = newHour
                alarm.minute = newMinute
                alarm.second = 0
                alarm.isActive = True
                # Permitimos que el siguiente disparo sea valido aunque caiga en
                # el mismo minuto que el ultimo registrado.
                self._lastFiredMinute = None
                return

    def checkDue(self, currentTime: tuple) -> Optional[Alarm]:
        """Devuelve la alarma que coincide con (hora, minuto) actuales, o None.

        Ignoramos los segundos: la alarma dispara apenas el motor entra al
        minuto objetivo. Esto permite que pausar y reanudar dentro del minuto
        siga disparando la alarma.
        """
        currentHour, currentMinute, _unusedSecond = currentTime
        currentMinuteKey = (currentHour, currentMinute)
        if currentMinuteKey == self._lastFiredMinute:
            return None
        for node in self._alarmList:
            alarm = node.getTime()
            if alarm.isActive and alarm.hour == currentHour and alarm.minute == currentMinute:
                self._lastFiredMinute = currentMinuteKey
                # Modo one-shot: la alarma queda desactivada tras sonar.
                alarm.isActive = False
                return alarm
        return None
